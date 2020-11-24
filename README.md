# SSP-Scheduler
SSP-Scheduler is a web application that helps students in creating their desired schedules with many preferences in no time.

## Table of Contents
  - [Motivation](#motivation)
  - [Demo](#demo)
  - [Features](#features)
  - [Run locally](#run-the-app-locally)
  - [Built with](#built-with)
  - [Related projects](#related-projects)

## Motivation
By developing this application we solved a big problem for us, we were spending a lot of time at the beginning of each semester in creating our schedules with our preferences like shrinking the gaps between learning slots during the day, choosing specific instructors and many others.\
So the main motives that derived us to develop this application was:
* Solving our problem with our software knowledge to make our lives easier which is the purpose of software after all.
* Help our colleagues who are facing the same problem.
* Level up our problem-solving, coding and software development skills and push them further.

## Demo
**You can use the app using [this link](https://sspscheduler.herokuapp.com/)**

![](static/images/scheduler.gif)

## Features
* Priorities of instructors from avoid this instructor to give this instructor the highest priority.
* Schedule density minimum or maximum days during the week.
* Preferred days off that the scheduler will try to keep them empty.
* Alternative schedule for each course in the best schedule to provide backup schedules in case the student wasn't able to register the best schedule
* Register different courses from different semesters in the same department

## Run the app locally
### Initial Setup
Install dependencies:
```
pip install -r requirements.txt
```

### Run App
```
python manage.py runserver
```

## Built with
[Django](https://www.djangoproject.com)\
[Bootstarp](https://getbootstrap.com)\
[jQuery](https://jquery.com/)

## TODO
* Creating a C/C++ library for schedules generation.
* Using multithreading to improve the generation performance.
* Auto schedule registration functionality.


## Related projects
[Database-Filler](https://github.com/ahmedfawzy98/Database-filler) is a sub-project that responsible for feeding the SSP-Scheduler with the needed data to work with.\
[SSP-Scheduler old](https://github.com/amohamed97/SSPScheduler) is the first version of this project that built with Java.

