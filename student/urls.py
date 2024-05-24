from django.urls import path
from .views import *

urlpatterns = [
    path('courseregistration', courseRegistration, name='courseRegister'),
    path('currentScore', currentSheet),
    path('feedback', studentFeedback, name='feedback'),
    path('data', pastData),
    path('fetchTeacher', fetchTeacher)
]
