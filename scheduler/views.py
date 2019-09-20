from django.shortcuts import render
from operator import attrgetter
# Create your views here.
from scheduler.Controller.Controller import Controller
from scheduler.Controller.Input import Input
from scheduler.Controller import Input as input_file
import copy
from scheduler.Classes.Course import Course

import time



def select_courses(request):
    if 'courses' not in request.session:
        request.session['courses'] = []
    if request.method == 'POST':
        # input_file.department = request.POST.get('department')
        request.session['department'] = request.POST.get('department')
    request.session['courses'].clear()
    request.session.modified = True
    database = Input(request.session['department'])
    return render(request, 'index.html', context={"courses": database.getCoursesOnly(),
                                                  'term_numbers': database.term_numbers})


def index(request):
    input = Input(request.session['department'])
    if request.method == "GET":
        dict = {}
        if len(request.session['courses']) > 0:
            courses = input.getCourses(request.session['courses'])
            courses.sort(key=attrgetter('name'))
            dict["courses"] = courses
            dict["coursesNum"] = len(courses)
            i = 0
            while i < 6:
                j = 0
                while j < 12:
                    dict['p' + str(i) + '_' + str(j)] = "<td></td>"
                    j += 1
                i += 1
            return render(request, 'schedule.html', context=dict)
        else:
            return render(request, 'illegal.html')
    else:
        priority = []
        dict = {}
        controller = Controller()
        allcourses = input.courses
        # "selection" indicates that the request is from courses selection page
        if request.POST.get("submit") == "selection":
            if int(request.POST.get("hoursTaken")) < 12:
                return render(request, "illegal.html")
            if len(request.session['courses']) > 0:
                # clean_priority(request.session['courses'])
                request.session['courses'].clear()
                request.session.modified = True

            for course in allcourses:
                if request.POST.get(course.name) == "on":
                    request.session['courses'].append(course.name)
            request.session.modified = True
            courses = input.getCourses(request.session['courses'])
            dict["courses"] = courses
            dict["coursesNum"] = len(courses)
            courses.sort(key=attrgetter('name'))
            i = 0
            while i < 6:
                j = 0
                while j < 12:
                    dict['p' + str(i) + '_' + str(j)] = "<td></td>"
                    j += 1
                i += 1
            return render(request, 'schedule.html', context=dict)
        # "generation" indicates that the request is from the current page */schedule/
        elif request.POST.get("submit") == "generation":
            courses = input.getCourses(request.session['courses'])
            start_time = time.time()
            # clean_priority(courses)
            dict["courses"] = courses
            dict["coursesNum"] = len(courses)
            for course in courses:
                if request.POST.get(course.name) != "Any Instructor":
                    priority.append((course.name, request.POST.get(course.name)))
            for pr in priority:
                for course in courses:
                    if pr[0] == course.name:
                        for inst in course.instructors:
                            if pr[1] == inst.name:
                                inst.priority = int(request.POST.get(course.name + "Pr"))
                                course.priority = int(request.POST.get(course.name + "Pr"))
            controller.courses = copy.deepcopy(courses)
            controller.makeSchedule()
            schedule = controller.schedule.schedule
            alternatives = [x.schedule for x in controller.alternatives]
            allSchedules = [schedule] + alternatives
            schedulesHTML = [[[None for x in range(12)] for y in range(6)] for z in range(len(allSchedules))]

            for ind,sch in enumerate(allSchedules):
                i = 0
                while i < 6:
                    j = 0
                    while j < 12:
                        if sch[i][j] is not None:

                            if sch[i][j].periodType == "Lecture":
                                schedulesHTML[ind][i][j] = "<td bgcolor='#FFE9E7' colspan='" + str(
                                    sch[i][j].length) + "'>" + sch[i][j].courseName + "<br>" + sch[i][
                                                                        j].instName + "</td>"
                            elif sch[i][j].periodType == "Tut":
                                schedulesHTML[ind][i][j] = "<td bgcolor='#d1e7f7' >" + sch[i][
                                    j].courseName + "<br>" + sch[i][j].instName + "</td>"
                            else:
                                schedulesHTML[ind][i][j] = "<td bgcolor='#BDFFFF'>" + sch[i][
                                    j].courseName + "<br>" + sch[i][j].instName + "</td>"
                            for jj in range(1,sch[i][j].length):
                                schedulesHTML[ind][i][j+jj] = ""
                            j += sch[i][j].length
                        else:
                            schedulesHTML[ind][i][j] = "<td bgcolor='#FFFFFF'></td>"
                            j += 1

                    i += 1
            dict["coursesNames"] = [list(a) for a in zip(["Best"]+controller.altCourses,["best"]+
                                                         [ c.replace(' ','') for c in  controller.altCourses])]
            courses.sort(key=attrgetter('name'))
            print("Total Time:--- %s seconds ---" % (time.time() - start_time))
            dict["allSchedules"] = [list(a) for a in zip(schedulesHTML,["best"]+[ c.replace(' ','') for c in  controller.altCourses])]
            return render(request, 'schedule.html', context=dict)


def select_department(request):
    if request.method == 'GET':
        return render(request, 'department.html')
    # else:
    #     input_file.department = request.POST.get('department')
    #     return select_courses(request)


def clean_priority(coursesf):
    for course in coursesf:
        course.priority = 0
        for inst in course.instructors:
            inst.priority = 0
