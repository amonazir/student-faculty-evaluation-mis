from django.urls import path
from .views import *

urlpatterns = [
    # path('adminnis',administrator),
    path('fetchstudent', fetchStudent),
    path('instructor', manageInstructor, name='instructor'),
    path('duplicateEID', duplicateEID),
    path('course', manageCourse),
    path('course/edit/<str:cid>', editCourse),
    path('registrationSetup', registrationSetup),
    path('feedbacks', manage_feedbacks),
    path('adminSettings', admin_settings, name='settings'),
    path('stopRegistration', stopRegistrations),
    path('', dashboard, name='dashboard')
]
