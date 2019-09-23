from django.shortcuts import render
from django.http import JsonResponse
from operator import attrgetter
from scheduler.Controller.Controller import Controller
import copy
from django.template.loader import render_to_string
from scheduler.models import *
from django.db.models import Q

import time

# Create your views here.


def select_courses(request):
    if 'courses' not in request.session:
        request.session['courses'] = []
    if request.method == 'POST':
        request.session['department'] = request.POST.get('department')
    request.session['courses'].clear()
    request.session.modified = True
    courses = Course.objects.all().filter(Q(department=request.session['department']) | Q(term=11))
    term_numbers = list(dict.fromkeys([x['term'] for x in Course.objects.all().values('term')]))
    return render(request, 'index.html', context={"courses": courses, 'term_numbers': term_numbers})


def index(request):
    allcourses = Course.objects.all().filter(Q(department=request.session['department']) | Q(term=11))
    if request.method == "GET":
        dict = {}
        if len(request.session['courses']) > 0:
            courses = [course for course in allcourses if course.name in request.session['courses']]
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
            courses = [course for course in allcourses if course.name in request.session['courses']]
            dict["courses"] = courses
            instructors = {}
            for course in courses:
                instructors[course.id] = Instructor.objects.all().filter(course__pk=course.id)

            dict['instructors'] = instructors
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


def generate_schedules(request):
    allcourses = list(Course.objects.all().filter(Q(department=request.session['department']) | Q(term=11)))
    priority = []
    dict = {}
    controller = Controller()
    courses = [course for course in allcourses if course.name in request.session['courses']]
    # clean_priority(courses)
    dict["courses"] = courses
    dict["coursesNum"] = len(courses)
    for course in courses:
        if request.POST.get(course.name) != "Any Instructor":
            priority.append((course.name, request.POST.get(course.name)))
    for pr in priority:
        for course in courses:
            if pr[0] == course.name:
                for inst in course.instructors():
                    if pr[1] == inst.name:
                        inst.priority = int(request.POST.get(course.name + "Pr"))
                        course.priority = int(request.POST.get(course.name + "Pr"))
    start_time = time.time()
    for course in courses:
        course.build()
    print("Building time:--- %s seconds ---" % (time.time() - start_time))
    controller.courses = copy.deepcopy(courses)
    start_time = time.time()
    controller.makeSchedule()
    print("Building tree time:--- %s seconds ---" % (time.time() - start_time))
    print("FUNC TIME : %s" % controller.func_runtime)
    schedule = controller.schedule.schedule
    alternatives = [x.schedule for x in controller.alternatives]
    allSchedules = [schedule] + alternatives
    schedulesHTML = [[[None for x in range(12)] for y in range(6)] for z in range(len(allSchedules))]

    for ind, sch in enumerate(allSchedules):
        i = 0
        while i < 6:
            j = 0
            while j < 12:
                if sch[i][j] is not None:

                    if sch[i][j].periodType == "Lecture":
                        schedulesHTML[ind][i][j] = "<td bgcolor='#FFE9E7' colspan='" + str(
                            sch[i][j].length()) + "'>" + sch[i][j].courseName() + "<br>" + sch[i][
                                                       j].instName() + "</td>"
                    elif sch[i][j].periodType == "Tut":
                        schedulesHTML[ind][i][j] = "<td bgcolor='#d1e7f7' >" + sch[i][
                            j].courseName() + "<br>" + sch[i][j].instName() + "</td>"
                    else:
                        schedulesHTML[ind][i][j] = "<td bgcolor='#BDFFFF'>" + sch[i][
                            j].courseName() + "<br>" + sch[i][j].instName() + "</td>"
                    for jj in range(1, sch[i][j].length()):
                        schedulesHTML[ind][i][j + jj] = ""
                    j += sch[i][j].length()
                else:
                    schedulesHTML[ind][i][j] = "<td bgcolor='#FFFFFF'></td>"
                    j += 1

            i += 1
    dict["coursesNames"] = [list(a) for a in zip(["Best"] + controller.altCourses, ["best"] +
                                                 [c.replace(' ', '') for c in controller.altCourses])]
    courses.sort(key=attrgetter('name'))
    dict["allSchedules"] = [list(a) for a in
                            zip(schedulesHTML, ["best"] + [c.replace(' ', '') for c in controller.altCourses])]
    # return render(request, 'schedule.html', context=dict)
    x = render_to_string(template_name='schedules.html', context=dict)
    print("HELLO")
    data = {
        'text': x
    }
    return JsonResponse(data)


# def ajaxTest(request):
#     data = {
#         'text': request.POST.get("Programming 2" + "Pr")
#     }
#     return JsonResponse(data)

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
