from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class currentRegistrations(models.Model):
    registrationStart = models.DateTimeField(default=now, blank=True)
    liveRegistration = models.BooleanField(default=False)


class branches(models.Model):
    # Branches in that perticular institute
    branchName = models.CharField(max_length=50)
    subcode = models.CharField(max_length=50)
    rollnocode = models.CharField(max_length=50)

    def __str__(self):
        return self.subcode


class administrator(models.Model):
    name = models.CharField(max_length=50)
    employeeID = models.CharField(max_length=20)
    mobileNumber = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)


class teacherProfile(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    MobileNumber = models.CharField(max_length=50, null=True, blank=True)
    employeeId = models.CharField(max_length=50)
    email = models.CharField(max_length=50,  null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    rating = models.FloatField(default=0)
    department = models.ForeignKey(
        branches, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.employeeId


class evaluationScheme(models.Model):
    name = models.CharField(max_length=50)
    weightage = models.CharField(max_length=20)
    max_score = models.CharField(max_length=10)


class sessionYear(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class Subject(models.Model):
    # Creating a subject, only addministrator can create this.
    subjectId = models.CharField(max_length=50)
    subjectName = models.CharField(max_length=100)
    credits = models.IntegerField()
    teachers = models.ManyToManyField(teacherProfile, null=True, blank=True)
    subjectType = models.CharField(max_length=20)
    offeredSem = models.CharField(max_length=20)
    totalSeats = models.IntegerField(default=0)

    def __str__(self):
        return self.subjectId


class sessionSubject(models.Model):
    # year in the session.
    remainingSeats = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    evaluation = models.ManyToManyField(
        evaluationScheme, null=True, blank=True)
    schemeSet = models.BooleanField(default=False)
    sessionName = models.ForeignKey(sessionYear, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.subject.subjectId


class scoreCard(models.Model):
    # This table is to give score to each evalution module created by the instructor.
    evaluationMethod = models.ForeignKey(
        evaluationScheme, on_delete=models.CASCADE)
    Score = models.CharField(max_length=30)


class studentSessionsheet(models.Model):
    # table to store the score of student's subject
    subject = models.ForeignKey(sessionSubject, on_delete=models.CASCADE)
    scoreSheet = models.ManyToManyField(scoreCard, null=True, blank=True)
    total = models.CharField(max_length=20, null=True, blank=True)
    grade = models.CharField(max_length=20, null=True, blank=True)
    isPassed = models.BooleanField(default=False)

    # sessionYear = models.ForeignKey(sessionYear, on_delete = models.CASCADE)


class gradeSheet(models.Model):
    # Score sheet, taking additional to
    subjects = models.ManyToManyField(studentSessionsheet)
    current = models.BooleanField(default=True)


class studentProfile(models.Model):
    # Building student profile, initially with name and email and then ask them to complete their profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    fatherName = models.CharField(max_length=50, null=True, blank=True)
    MothersName = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    MobileNumber = models.CharField(max_length=50, null=True, blank=True)
    rollNumber = models.CharField(max_length=50)
    branch = models.CharField(max_length=10, default=None)
    degreeType = models.CharField(max_length=15, default=None)
    Address = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    parentContact = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    scoreSheet = models.ManyToManyField(gradeSheet, null=True, blank=True)
    currentSem = models.CharField(max_length=20, default='0')
    admissionYear = models.CharField(max_length=20)
    currentStudent = models.BooleanField(default=True)
    backlogs = models.IntegerField(default=0)
    currentSemRegister = models.BooleanField(default=False)

    def __str__(self):
        return self.rollNumber


class loginMode(models.Model):
    # Since we are using single login page for the authentication, this table helps in differentiating the type of user logging into the system, whether instructor, student or the administrator, and administrator has the complete priviliges to view, and change these fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)


class feedback(models.Model):
    # Not taking student details to make the feedback completely anonymous.
    point = models.IntegerField(default=0)
    teacher = models.ForeignKey(teacherProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        sessionSubject, on_delete=models.CASCADE, null=True)
    description = models.TextField()
