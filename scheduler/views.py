from django.shortcuts import render
from operator import attrgetter
# Create your views here.
from scheduler.Controller.Controller import Controller
from scheduler.Controller.Input import Input

courses = []


def select_courses(request):
    courses.clear()
    database = Input()
    return render(request, 'index.html', context={"courses": database.getCoursesOnly()})


def index(request):
    if request.method == "GET":
        dict = {}
        if len(courses) > 0:
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
        input = Input()
        allcourses = input.courses
        # "selection" indicates that the request is from courses selection page
        if request.POST.get("submit") == "selection":
            if int(request.POST.get("hoursTaken")) < 12:
                return render(request, "illegal.html")
            if len(courses) > 0:
                clean_priority(courses)
                courses.clear()

            for course in allcourses:
                if request.POST.get(course.name) == "on":
                    courses.append(course)
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
            clean_priority(courses)
            dict["courses"] = courses
            dict["coursesNum"] = len(courses)
            for course in courses:
                if request.POST.get(course.name) != "Select Instructor":
                    priority.append((course.name, request.POST.get(course.name)))
            for pr in priority:
                for course in courses:
                    if pr[0] == course.name:
                        for inst in course.instructors:
                            if pr[1] == inst.name:
                                inst.priority = int(request.POST.get(course.name + "Pr"))
                                course.priority = int(request.POST.get(course.name + "Pr"))
            controller.courses = courses
            controller.makeSchedule()
            schedule = controller.schedule.schedule
            i = 0
            while i < 6:
                j = 0
                while j < 12:
                    if schedule[i][j] is not None:

                        if schedule[i][j].periodType == "Lecture":
                            dict['p' + str(i) + '_' + str(j)] = "<td bgcolor='#FFE9E7' colspan='" + str(
                                schedule[i][j].length) + "'>" + schedule[i][j].courseName + "<br>" + schedule[i][
                                                                    j].instName + "</td>"
                        elif schedule[i][j].periodType == "Tut":
                            dict['p' + str(i) + '_' + str(j)] = "<td bgcolor='#d1e7f7' >" + schedule[i][
                                j].courseName + "<br>" + schedule[i][j].instName + "</td>"
                        else:
                            dict['p' + str(i) + '_' + str(j)] = "<td bgcolor='#BDFFFF'>" + schedule[i][
                                j].courseName + "<br>" + schedule[i][j].instName + "</td>"
                        j += schedule[i][j].length
                    else:
                        dict['p' + str(i) + '_' + str(j)] = "<td></td>"
                        j += 1

                i += 1
            courses.sort(key=attrgetter('name'))
            return render(request, 'schedule.html', context=dict)


def clean_priority(coursesf):
    for course in coursesf:
        course.priority = 0
        for inst in course.instructors:
            inst.priority = 0
