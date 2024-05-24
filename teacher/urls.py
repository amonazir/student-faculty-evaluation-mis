from django.urls import path
from .views import *

urlpatterns = [
    # path('teacher', edit_profile, name='editProfile'),
    path('manageCourses/<str:session>', manage_courses, name='manageCourses'),
    path('manageCourses', manage_courses_wrap),
    path('showFeedback', show_feedback, name='showFeedback'),
    path('grading/<str:session>', set_grading, name='grading'),
    path('grading', set_grading_wrap, name='grading'),
    path('submitEvalModules', set_eval_modules),
    path('fetchStudents', fetchStudents),
    path('submitstudentMark', submitStudentMark)
]
