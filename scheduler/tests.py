from django.test import TestCase

# Create your tests here.
from scheduler.Controller.Controller import Controller

if __name__ == '__main__':
    controller = Controller()
    controller.makeSchedule()
    controller.schedule.printSchedule()
    for i in range(len(controller.alternatives)):
        print('---------------------------------------------------------------------------------------------------' +
              '--------------------------------------------------------------------------' +
              '------------------------------------------------------------------------------------------------------' +
              '-------------------------------------------------------------------------------' +
              '-------------------------------------------------------' +
              '--------------------------------------------------')
        controller.alternatives[i].printSchedule()
