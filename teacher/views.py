from django.shortcuts import render, redirect
from django.http import JsonResponse
from stem.models import *
from django.core.files.storage import FileSystemStorage
from stem.models import *
from django.contrib.auth.decorators import login_required
import json


@login_required
def edit_profile(request):
    if request.method == 'POST':
        photo = request.FILES['photo']
        fs = FileSystemStorage(location="media/profilePhoto/")
        filename = fs.save(photo.name, photo)
        teacher = teacherProfile.objects.get(user=request.user)
        teacher.firstName = request.POST.get('fname')
        teacher.lastName = request.POST.get('lname')
        teacher.dob = request.POST.get('dob')
        teacher.MobileNumber = request.POST.get('mobileNo')
        teacher.email = request.POST.get('secondaryEmail')
        teacher.photo = filename
        teacher.save()
        return redirect('/')

    teacher = teacherProfile.objects.get(user=request.user)
    return render(request, 'teacherHome.html', context={'data': teacher})


@login_required
def manage_courses(request, session):
    print(request.user.username)
    #sessionSubject.objects.get(subject = subjs)
    if loginMode.objects.get(user=request.user).type == 'teacher':
        course = []
        sess = sessionYear.objects.get(year=session)
        courses = Subject.objects.all()
        for subjs in courses:
            teachers = subjs.teachers.all()
            for teacher in teachers:
                if teacher.user == request.user:
                    course.append(sessionSubject.objects.get(
                        subject=subjs, sessionName=sess))

        teacher = teacherProfile.objects.get(user=request.user)
        return render(request, 'manageCourses.html', context={'courses': course, 'data': teacher})

    return redirect('error')


@login_required
def show_feedback(request):
    if loginMode.objects.get(user=request.user).type == 'teacher':
        teacher = teacherProfile.objects.get(user=request.user)
        feed_data = feedback.objects.filter(teacher=teacher)
        return render(request, 'teacherFeedback.html', context={'data': teacher, 'feedbacks': feed_data})

    return redirect('error')


@login_required
def set_grading(request, session):
    if loginMode.objects.get(user=request.user).type == 'teacher':
        course = []
        sess = sessionYear.objects.get(year=session)
        courses = Subject.objects.all()
        for subjs in courses:
            teachers = subjs.teachers.all()
            for teacher in teachers:
                if teacher.user == request.user:
                    course.append(sessionSubject.objects.get(
                        subject=subjs, sessionName=sess))

        teacher = teacherProfile.objects.get(user=request.user)
        return render(request, 'teacherGrading.html', context={'courses': course, 'data': teacher})

    return redirect('error')


@login_required
def set_eval_modules(request):
    if request.method == 'POST':
        if loginMode.objects.get(user=request.user).type == 'teacher':
            data = json.loads(request.body.decode('utf-8'))
            cid = data['courseId']
            session = data['session']
            sess = sessionYear.objects.get(year=session)
            sub = Subject.objects.get(subjectId=cid)
            print(sub)
            ss = sessionSubject.objects.get(subject=sub, sessionName=sess)
            sss = studentSessionsheet.objects.filter(subject=ss)
            if ss.schemeSet == False:
                del data['courseId']
                for num in data.keys():
                    scheme = evaluationScheme.objects.create(
                        name=data[num]['evname'], weightage=data[num]['weightage'], max_score=data[num]['score'])
                    for x in sss:
                        sc = scoreCard.objects.create(
                            evaluationMethod=scheme, Score=0)
                        x.scoreSheet.add(sc)
                        x.save()

                    ss.evaluation.add(scheme)
                    ss.save()

                ss.schemeSet = True
                ss.save()

                return JsonResponse({'type': 'success'})

    return JsonResponse({'type': 'error'})


@login_required
def manage_courses_wrap(request):
    if loginMode.objects.get(user=request.user).type == 'teacher':
        if request.method == "POST":
            sess = request.POST.get('session')
            return redirect('/manageCourses/'+sess)

        sessions = sessionYear.objects.all()
        teacher = teacherProfile.objects.get(user=request.user)
        return render(request, 'selectSession.html', context={'session': sessions, 'm': True, 'g': False, 'data': teacher})

    return redirect('error')


@login_required
def set_grading_wrap(request):
    if loginMode.objects.get(user=request.user).type == 'teacher':
        if request.method == "POST":
            sess = request.POST.get('session')
            return redirect('/grading/'+sess)

        sessions = sessionYear.objects.all()
        teacher = teacherProfile.objects.get(user=request.user)
        return render(request, 'selectSession.html', context={'session': sessions, 'm': False, 'g': True, 'data': teacher})

    return redirect('error')


@login_required
def fetchStudents(request):
    data = json.loads(request.body.decode('utf-8'))
    session = data['session']
    cid = data["cid"]

    subj = sessionSubject.objects.get(subject=Subject.objects.get(
        subjectId=cid), sessionName=sessionYear.objects.get(year=session))
    data = []

    for stu in studentProfile.objects.all():
        for x in stu.scoreSheet.all():
            for k in x.subjects.all():
                if k.subject == subj:
                    temp = {
                        'name': stu.firstName + " " + stu.lastName,
                        'roll': stu.rollNumber,
                        'id': k.id
                    }

                    data.append(temp)

    print(data)
    return JsonResponse({'data': data})


@login_required
def submitStudentMark(request):
    if loginMode.objects.get(user=request.user).type == 'teacher':
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))

            for sid in data.keys():
                sheet = studentSessionsheet.objects.get(id=sid)
                scs = sheet.scoreSheet.all()
                sum_score = 0
                for x in scs:
                    for k in data[sid].keys():
                        # print(x.evaluationMethod)
                        if x.evaluationMethod.id == int(k):
                            print(k,x)
                            temp = scoreCard.objects.get(evaluationMethod = evaluationScheme.objects.get(id = int(k)))
                            temp.Score = data[sid][k]
                            temp.save()
                            sum_score += int(data[sid][k])

                sheet.total = sum_score
                sheet.save()

            return JsonResponse({"type": "success"})

        return JsonResponse({"type": "error"})
