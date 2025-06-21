from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings



class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    stage = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    dob = models.CharField(max_length=50, blank=True, null=True)
    disability = models.CharField(max_length=200, blank=True, null=True)
    blood_group = models.CharField(max_length=200,  blank=True, null=True)
    date_admitted = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_admitted']
        db_table = ''
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'All Students'
   

    def __str__(self):
        return self.user.username


class Teachers(models.Model):
    tid = models.IntegerField(unique=True)
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    othername = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    disability = models.CharField(max_length=200, blank=True, null=True)
    date_employed = models.DateTimeField(auto_now=True, blank=True, null=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ['-date_employed']
        db_table = ''
        managed = True
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.lastname} {self.firstname}"


class Departments(models.Model):
    did = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    hod = models.CharField(max_length=50, blank=True, null=True)
    assistant_hod = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    number_of_workers = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        db_table = ''
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title


class Subjects(models.Model):
    code = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        db_table = ''
        managed = True
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.title


class Stages(models.Model):
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.title


class Terms(models.Model):
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        db_table = ''
        managed = True
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return self.title


class Fees(models.Model):
    fid = models.IntegerField()
    fee = models.CharField(max_length=50)
    term = models.IntegerField()
    stage = models.IntegerField()
    amount = models.FloatField()
    bill_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-bill_date']
        db_table = ''
        managed = True
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'

    def __str__(self):
        return f"fees for {self.term } Class {self.stage }"


class FeeCollections(models.Model):
    fee = models.CharField(max_length=100)
    sid = models.IntegerField()
    amount = models.FloatField()
    paid = models.FloatField()
    arrears = models.FloatField(default=0.0)
    credit = models.FloatField(default=0.0)
    bill_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-bill_date']
        db_table = ''
        managed = True
        verbose_name = 'Fee Collection'
        verbose_name_plural = 'Fee Collections'

    def __str__(self):
        return f"{ self.sid }"


class Expenses(models.Model):
    item = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(default=0.0)
    bill_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return self.item


class Salaries(models.Model):
    staff = models.CharField(max_length=100)
    amount = models.FloatField(default=0.0)
    due_date = models.DateField()
    bill_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'

    def __str__(self):
        return self.staff


class Exams(models.Model):
    name = models.CharField(max_length=50)
    stage = models.CharField(max_length=20)
    teacher = models.CharField(max_length=50)
    invigilators = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Exam List'
        verbose_name_plural = 'Exam Lists'

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    subject = models.CharField(max_length=150)
    day = models.CharField(max_length=50)
    teacher = models.CharField(max_length=150, blank=True, null=True)
    stage = models.CharField(max_length=50)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Time Table'
        verbose_name_plural = 'Time Table'

    def __str__(self):
        return f"time table"



class Result(models.Model):
    sid = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default=" ")
    position = models.CharField(max_length=100, default=" ")
    promoted_to = models.CharField(max_length=100, default=" ")
    term = models.CharField(max_length=100)
    year = models.CharField(max_length=100, default=" ")
    number_on_roll = models.CharField(max_length=100, default=" ")
    boys = models.CharField(max_length=100, default=" ")
    girls = models.CharField(max_length=100, default=" ")
    attendance = models.CharField(max_length=100, default=" ")
    total_attendance = models.CharField(max_length=100, default=" ")
    teachers_comment = models.CharField(max_length=300, default=" ")
    next_term = models.CharField(max_length=100, default=" ")
    report = models.FileField(upload_to='resultfiles',  default=" ")

    #first subject
    s1 = models.CharField(max_length=100, default=" ")
    s1ClassScore = models.CharField(max_length=100, default=" ")
    s1ExamsScore = models.CharField(max_length=100, default=" ")
    s1MidTerm = models.CharField(max_length=100, default=" ")
    s1Total = models.CharField(max_length=100, default=" ")
    s1Grade = models.CharField(max_length=100, default=" ")
    s1Comment = models.CharField(max_length=100, default=" ")

    s2 = models.CharField(max_length=100, default=" ")
    s2ClassScore = models.CharField(max_length=100, default=" ")
    s2ExamsScore = models.CharField(max_length=100, default=" ")
    s2MidTerm = models.CharField(max_length=100, default=" ")
    s2Total = models.CharField(max_length=100, default=" ")
    s2Grade = models.CharField(max_length=100, default=" ")
    s2Comment = models.CharField(max_length=100, default=" ")

    s3 = models.CharField(max_length=100, default=" ")
    s3ClassScore = models.CharField(max_length=100, default=" ")
    s3ExamsScore = models.CharField(max_length=100, default=" ")
    s3MidTerm = models.CharField(max_length=100, default=" ")
    s3Total = models.CharField(max_length=100, default=" ")
    s3Grade = models.CharField(max_length=100, default=" ")
    s3Comment = models.CharField(max_length=100, default=" ")

    s4 = models.CharField(max_length=100, default=" ")
    s4ClassScore = models.CharField(max_length=100, default=" ")
    s4ExamsScore = models.CharField(max_length=100, default=" ")
    s4MidTerm = models.CharField(max_length=100, default=" ")
    s4Total = models.CharField(max_length=100, default=" ")
    s4Grade = models.CharField(max_length=100, default=" ")
    s4Comment = models.CharField(max_length=100, default=" ")

    s5 = models.CharField(max_length=100, default=" ")
    s5ClassScore = models.CharField(max_length=100, default=" ")
    s5ExamsScore = models.CharField(max_length=100, default=" ")
    s5MidTerm = models.CharField(max_length=100, default=" ")
    s5Total = models.CharField(max_length=100, default=" ")
    s5Grade = models.CharField(max_length=100, default=" ")
    s5Comment = models.CharField(max_length=100, default=" ")

    s6 = models.CharField(max_length=100, default=" ")
    s6ClassScore = models.CharField(max_length=100, default=" ")
    s6ExamsScore = models.CharField(max_length=100, default=" ")
    s6MidTerm = models.CharField(max_length=100, default=" ")
    s6Total = models.CharField(max_length=100, default=" ")
    s6Grade = models.CharField(max_length=100, default=" ")
    s6Comment = models.CharField(max_length=100, default=" ")

    s7 = models.CharField(max_length=100, default=" ")
    s7ClassScore = models.CharField(max_length=100, default=" ")
    s7ExamsScore = models.CharField(max_length=100, default=" ")
    s7MidTerm = models.CharField(max_length=100, default=" ")
    s7Total = models.CharField(max_length=100, default=" ")
    s7Grade = models.CharField(max_length=100, default=" ")
    s7Comment = models.CharField(max_length=100, default=" ")

    s8 = models.CharField(max_length=100, default=" ")
    s8ClassScore = models.CharField(max_length=100, default=" ")
    s8ExamsScore = models.CharField(max_length=100, default=" ")
    s8MidTerm = models.CharField(max_length=100, default=" ")
    s8Total = models.CharField(max_length=100, default=" ")
    s8Grade = models.CharField(max_length=100, default=" ")
    s8Comment = models.CharField(max_length=100, default=" ")

    s9 = models.CharField(max_length=100, default=" ")
    s9ClassScore = models.CharField(max_length=100, default=" ")
    s9ExamsScore = models.CharField(max_length=100, default=" ")
    s9MidTerm = models.CharField(max_length=100, default=" ")
    s9Total = models.CharField(max_length=100, default=" ")
    s9Grade = models.CharField(max_length=100, default=" ")
    s9Comment = models.CharField(max_length=100, default=" ")

    s10 = models.CharField(max_length=100, default=" ")
    s10ClassScore = models.CharField(max_length=100, default=" ")
    s10ExamsScore = models.CharField(max_length=100, default=" ")
    s10MidTerm = models.CharField(max_length=100, default=" ")
    s10Total = models.CharField(max_length=100, default=" ")
    s10Grade = models.CharField(max_length=100, default=" ")
    s10Comment = models.CharField(max_length=100, default=" ")

    s11 = models.CharField(max_length=100, default=" ")
    s11ClassScore = models.CharField(max_length=100, default=" ")
    s11ExamsScore = models.CharField(max_length=100, default=" ")
    s11MidTerm = models.CharField(max_length=100, default=" ")
    s11Total = models.CharField(max_length=100, default=" ")
    s11Grade = models.CharField(max_length=100, default=" ")
    s11Comment = models.CharField(max_length=100, default=" ")

    total = models.CharField(max_length=100, default=" ")

    added_by = models.CharField(max_length=100, default='Admin')
    date_added = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-date_added']
        db_table = ''
        managed = True
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return f"ID: { self.sid }, Class: { self.stage }, { self.term } Term Result"


class TeacherAttendances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    stage = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    time_start = models.CharField(max_length=20)
    time_end = models.CharField(max_length=20)

    class Meta:
        ordering = ['-date']
        db_table = ''
        managed = True
        verbose_name = 'Teacher Attendance'
        verbose_name_plural = 'Teacher Attendances'

    def __str__(self):
        return self.user.username