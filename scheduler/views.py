from django.shortcuts import render
from django.http import JsonResponse
from operator import attrgetter
from scheduler.Controller.Controller import Controller
import copy
from django.template.loader import render_to_string
from scheduler.models import *
from django.db.models import Q

import time


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
            if len(request.session['courses']) > 0:
                # clean_priority(request.session['courses'])
                request.session['courses'].clear()
                request.session.modified = True

            for course in allcourses:
                if request.POST.get(course.name) == "on":
                    request.session['courses'].append(course.name)
            request.session.modified = True
            courses = [course for course in allcourses if course.name in request.session['courses']]
            credit_hours = 0
            for course in courses:
                credit_hours+= course.creditHours
            if credit_hours < 12 or credit_hours > 21 :
                dict['error_msg'] = "Insufficient credit hours taken. At least 12 credit hours is required " \
                                    "<a href=\"/courses\">here</a>." if credit_hours < 12 else "Too many credit hours taken. At maximum 21 credit hours is allowed " \
                                    "<a href=\"/courses\">here</a>."
                return render(request, "illegal.html", context= dict)

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
    for course in courses:
        course.build()
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
    days = ['sat-day', 'sun-day', 'mon-day', 'tue-day', 'wed-day', 'thu-day']
    offdays = []
    alt_yes = False
    for i in range(0,6):
        if request.POST.get(days[i]) == "selected":
            offdays.append(i)
    if request.POST.get('max-day') == "selected":
        controller.max_days = True
    if request.POST.get('alt-yes') == "selected":
        alt_yes = True

    dict["alt"] = alt_yes
    controller.alt_yes = alt_yes
    controller.offdays = offdays
    controller.courses = copy.deepcopy(courses)
    start_time = time.time()
    controller.create_schedules()
    print("Tree building time:--- %s seconds ---" % (time.time() - start_time))
    if controller.schedule is None:
        data = {
            'text': "<h4 id='all-schedules' class='text-center'>There's no possible schedule with your preferences</h4>"
        }
        return JsonResponse(data)
    best_schedule = controller.schedule.schedule
    # alternatives = [x.schedule for x in controller.alternatives]
    alternatives = []
    for alt in controller.alternatives:
        if alt:
            alternatives.append(alt.schedule)
        else:
            alternatives.append(None)

    if alt_yes:
        all_schedules = [best_schedule] + alternatives
    else:
        all_schedules = [best_schedule]
    schedules_html = [[[None for x in range(12)] for y in range(6)] for z in range(len(all_schedules))]

    for ind, sch in enumerate(all_schedules):
        if sch is None:
            schedules_html[ind][0][0] = "NOT FOUND"
            continue
        i = 0
        while i < 6:
            j = 0
            while j < 12:
                if sch[i][j] is not None:

                    if sch[i][j].periodType == "Lecture":
                        schedules_html[ind][i][j] = "<td bgcolor='#FFE9E7' colspan='" + str(
                            sch[i][j].length()) + "'>" + sch[i][j].courseName() + "<hr>" + sch[i][
                                                       j].instName() + "</td>"
                    elif sch[i][j].periodType == "Tut":
                        schedules_html[ind][i][j] = "<td bgcolor='#d1e7f7' >" + sch[i][
                            j].courseName() + "<hr>" + sch[i][j].instName() + "</td>"
                    else:
                        schedules_html[ind][i][j] = "<td bgcolor='#BDFFFF'>" + sch[i][
                            j].courseName() + "<hr>" + sch[i][j].instName() + "</td>"
                    for jj in range(1, sch[i][j].length()):
                        schedules_html[ind][i][j + jj] = ""
                    j += sch[i][j].length()
                else:
                    schedules_html[ind][i][j] = "<td bgcolor='#FFFFFF'></td>"
                    j += 1

            i += 1
    if alt_yes:
        dict["coursesNames"] = [list(a) for a in zip(["Best"] + controller.alt_courses, ["best"] +
                                                 [c.replace(' ', '') for c in controller.alt_courses])]
    else:
        dict["coursesNames"] = [list(a) for a in zip(["Best"], ["best"] )]
    courses.sort(key=attrgetter('name'))
    if alt_yes:
        dict["allSchedules"] = [list(a) for a in
                            zip(schedules_html, ["best"] + [c.replace(' ', '') for c in controller.alt_courses])]
    else:
        dict["allSchedules"] = [list(a) for a in
                                zip(schedules_html, ["best"])]
    x = render_to_string(template_name='schedules.html', context=dict)
    data = {
        'text': x
    }
    return JsonResponse(data)


def select_department(request):
    if request.method == 'GET':
        return render(request, 'department.html')


def clean_priority(coursesf):
    for course in coursesf:
        course.priority = 0
        for inst in course.instructors:
            inst.priority = 0
