from django.shortcuts import render

# Create your views here.
from scheduler.Controller.Controller import Controller


def index(request):
    dict = {}
    controller = Controller()
    controller.makeSchedule()
    schedule = controller.schedule.schedule
    i = 0
    while i < 6:
        j = 0
        while j < 12:
            if schedule[i][j] is not None:
                # print(str(i)+'-'+str(j))
                # while (schedule[i][j].courseName, schedule[i][j].periodType) == tempStr:
                #     span += 1
                #     tempStr = (schedule[i][j].courseName, schedule[i][j].periodType)
                # if (schedule[i][j].courseName, schedule[i][j].periodType) == tempStr:
                #     span += 1

                if schedule[i][j].periodType == "Lecture":
                    dict['p'+str(i)+'_'+str(j)] = "<td bgcolor='#FFE9E7' colspan='"+str(schedule[i][j].length)+"'>"+schedule[i][j].courseName+"<br>"+schedule[i][j].instName+"</td>"
                elif schedule[i][j].periodType == "Tut":
                    dict['p'+str(i)+'_'+str(j)] = "<td bgcolor='#d1e7f7' >"+schedule[i][j].courseName+"<br>"+schedule[i][j].instName+"</td>"
                else:
                    dict['p'+str(i)+'_'+str(j)] = "<td bgcolor='#BDFFFF'>"+schedule[i][j].courseName+"<br>"+schedule[i][j].instName+"</td>"
                j += schedule[i][j].length
            else:
                dict['p'+str(i)+'_'+str(j)] = "<td></td>"
                j += 1

        i += 1
    del controller
    return render(request, 'schedule.html', context=dict)
