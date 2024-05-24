from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from stem.models import *
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
import json


# Create your views here.
@login_required
def studentHome(request):
    if loginMode.objects.get(user=request.user).type == 'student':
        if request.method == 'POST':
            dob = request.POST.get('dob')
            mno = request.POST.get('mob')
            address = request.POST.get('address')
            email = request.POST.get('email')
            pcno = request.POST.get('pmob')
            pphoto = request.FILES['pphoto']
            student = studentProfile.objects.get(user=request.user)
            fs = FileSystemStorage(location="media/profilePhoto")
            filename = fs.save(pphoto.name, pphoto)
            student.dob = dob
            student.MobileNumber = mno
            student.Address = address
            student.email = email
            student.parentContact = pcno
            student.photo = filename
            student.save()

        student = studentProfile.objects.get(user=request.user)
        return render(request, 'studentHome.html', context={'data': student})

    return redirect('error')


@login_required
def courseRegistration(request):
    if loginMode.objects.get(user=request.user).type == 'student':
        student = studentProfile.objects.get(user=request.user)
        try:
            time_t = currentRegistrations.objects.all()[0].registrationStart
            print(time_t)
        except:
            return render(request, 'courseRegistraton.html', context={'start': False, 'Registration': True, 'data': student})

        if(student.currentSemRegister):
            return render(request, 'courseRegistraton.html', context={'start': False, 'Registration': True, 'data': student})

        elif time_t > now():
            return render(request, 'courseRegistraton.html', context={'start': False, 'time': str(time_t).split("+")[0], 'data': student})

        else:
            sem = student.currentSem
            semType = 'even' if int(sem) % 2 == 0 else 'odd'
            subjects = Subject.objects.filter(offeredSem=sem)

            # for F- Graded subjects!!

            sheets = student.scoreSheet.all()
            for score_sheet in sheets:
                if score_sheet.current == False:
                    subjs = score_sheet.subjects.all()
                    for i in subjs:
                        if i.isPassed == False:
                            sem = i.subject.subject.offeredSem
                            if int(sem) % 2 == 0 and semType == 'even':
                                subjects = subject | sem.subject.subject
                            elif int(sem) % 2 != 0 and semType == 'odd':
                                subjects = subject | sem.subject.subject

            if request.method == 'POST':
                CoursesID = request.POST
                courses = list(CoursesID.keys())
                courses.remove('csrfmiddlewaretoken')
                print(courses)
                sheet = gradeSheet.objects.create()
                for subject in courses:
                    sub = Subject.objects.get(subjectId=subject)
                    sessionsub = sessionSubject.objects.get(subject=sub)
                    print(sessionsub)
                    sss = studentSessionsheet.objects.create(
                        subject=sessionsub)
                    sheet.subjects.add(sss)
                    sheet.registered = True
                    sheet.save()
                    student.scoreSheet.add(sheet)
                student.currentSemRegister = True
                student.save()
                return redirect('courseRegister')

            return render(request, 'courseRegistraton.html', context={'start': True, 'subjects': subjects, 'data': student})

    return redirect('error')


@login_required
def currentSheet(request):
    if loginMode.objects.get(user=request.user).type == 'student':
        student = studentProfile.objects.get(user=request.user)
        scoresheet = student.scoreSheet.all()
        current = ''
        for i in scoresheet:
            if i.current == True:
                current = i

        y = current.subjects.all()
        print(y)
        return render(request, 'currentSemScore.html', context={'subs': y, 'prof': student})

    return redirect('error')


@login_required
def studentFeedback(request):
    if loginMode.objects.get(user=request.user).type == 'student':
        student = studentProfile.objects.get(user=request.user)
        print(request.POST)
        if request.method == 'POST':
            star = request.POST.get('star')
            print("----- ",star)
            teacher = teacherProfile.objects.get(
                employeeId=request.POST.get('teacher_name'))
            feedback.objects.create(point=int(star), teacher=teacher, subject=sessionSubject.objects.get(
                subject=Subject.objects.get(subjectId=request.POST.get('subName'))), description=request.POST.get('feedback'))

            return redirect('feedback')

        result = []
        for ss in student.scoreSheet.filter(current=True):
            subjects = ss.subjects.all()
            print(subjects)
            for sss in subjects:
                result.append(sss.subject)

        return render(request, 'studentFeedback.html', context={'data': student, 'teachers': result})

    return redirect('error')


@login_required
def pastData(request):
    return render(request, 'CumulativeResults.html')


@login_required
def fetchTeacher(request):
    if request.method == 'POST':
        scode = json.loads(request.body.decode('utf-8'))['subjectCode']
        print(scode)
        teachers = Subject.objects.get(subjectId=scode).teachers.all()
        res = {}
        for i in teachers:
            res[i.employeeId] = i.firstName + " " + i.lastName

        print(res)
        return JsonResponse(res)
