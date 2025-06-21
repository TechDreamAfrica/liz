from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from main.models import *
from django.contrib.auth.models import User, auth
from . import views
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io




def login(request):
    pagename = "User Login"


    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                messages.info(request, 'Admin Logged in Successfully')
                return redirect('admin-homepage')
            
            elif user.is_staff:
                auth.login(request, user)
                messages.info(request, 'Admin Logged in Successfully')
                return redirect('admin-homepage')
            
            else:
                messages.info(request, 'User Not an Admin: Can not Access This Page')
                return redirect('login')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    context = {
        'pagename':pagename
    }
    return render(request, 'lms/login.html', context)



def signup(request):
    if request.method == 'POST':
        pin = "#@Beyond_Me23"

        username = request.POST.get('userid')
        password = pin
        password2 = pin

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User ID Already Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.is_superuser=True
                user.save()
                messages.info(request, 'Admin Added Successfully')

                #log user in and redirect to settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('admin-homepage')

    pagename = 'Admin Register'

    context = {
        'pagename':pagename,
    }
    return render(request, 'register.html', context)



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


# Create your views here.
@login_required(login_url='login')
def index(request):
    user = get_object_or_404(User, username=request.user.username)
    pagename = "Site Admin"

    students = Students.objects.all()
    allStudents = students.count()

    if allStudents == 0:
        showStudents = "No Student"
    elif allStudents == 1:
        showStudents = f" { allStudents } Student"
    else:
        showStudents = f" { allStudents } Students"


    teachers = Teachers.objects.all()
    allTeachers = teachers.count()

    if allTeachers == 0:
        showTeachers = "No Teacher"
    elif allTeachers == 1:
        showTeachers = f" { allTeachers } Teacher"
    else:
        showTeachers = f" { allTeachers } Teachers"


    results = Result.objects.all()
    allResults = results.count()

    if allResults == 0:
        showResults = "No Result"
    elif allResults == 1:
        showResults = f" { allResults } Result"
    else:
        showResults = f" { allResults } Results"


    subjects = Subjects.objects.all()
    allSubjects = subjects.count()

    if allSubjects == 0:
        showSubjects = "No Subject"
    elif allSubjects == 1:
        showSubjects = f" { allSubjects } Subject"
    else:
        showSubjects = f" { allSubjects } Subjects"

    # Get all results for all students
    student_results = {}
    for student in students:
        student_results[student.user.username] = Result.objects.filter(sid=student.user.username)

    context = {
        'pagename':pagename,
        'showStudents':showStudents,
        'showTeachers':showTeachers,
        'showResults':showResults,
        'showSubjects':showSubjects,
        'students':students[:20],
        'results':results[:20],
        'student_results': student_results,
    }
    return render(request, 'lms/index.html', context)


#students area
@login_required(login_url='login')
def students(request):
    pagename = "Students Data"
    students = Students.objects.all()
    allStudents = students.count()

    if allStudents == 0:
        showStudents = "No Student"
    elif allStudents == 1:
        showStudents = f"{ allStudents } Student"
    else:
        showStudents = f"{ allStudents } Students"

    context = {
        'pagename':pagename,
        'students':students,
        'showStudents':showStudents
    }
    return render(request, 'lms/students.html', context)


@login_required(login_url='login')
def read_student(request, pk):
    get_user = get_object_or_404(User, username=pk)
    student = get_object_or_404(Students, user=get_user)
    pagename = f"Read Student | { get_user }"
    result = Result.objects.filter(sid=student.user.username)
    fee_collection = FeeCollections.objects.filter(sid=student.user.username)

    context = {
        'pagename':pagename,
        'student':student,
        'results':result,
        'fee_collection':fee_collection
    }
    return render(request, 'lms/read-student.html', context)


@login_required(login_url='login')
def edit_student(request, pk):
    get_user = get_object_or_404(User, username=pk)
    student = get_object_or_404(Students, user=get_user)
    pagename = f"Edit | { get_user } Data"
    pin = '123456789'
    stage = Stages.objects.all()

    if request.method == "POST":
        username = request.POST['sid']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        othername = request.POST['othername']
        gender = request.POST['gender']
        dob = request.POST['dob']
        religion = request.POST['religion']
        phone = request.POST['phone']
        blood_group = request.POST['bloodgroup']
        stage = request.POST['class']
        address = request.POST['address']
        disability = request.POST['disability']

        user_model = get_user
        student.user=user_model
        student.lastname=lastname
        student.firstname=firstname
        student.gender=gender
        student.dob=dob
        student.religion=religion
        student.phone=phone
        student.blood_group=blood_group
        student.stage=stage
        student.address=address
        student.disability=disability
        student.save()
        return redirect('read-student', pk)


    context = {
        'pagename':pagename,
        'student':student,
        'stages':stage
    }
    return render(request, 'lms/edit-student.html', context)



@login_required(login_url='login')
def add_student(request):
    pagename = "Add Student"
    stage = Stages.objects.all()

    if request.method == "POST":
        username = request.POST['sid']
        lastname = request.POST['lastname'].upper()
        firstname = request.POST['firstname'].upper()
        gender = request.POST['gender'].upper()
        dob = request.POST['dob'].upper()
        religion = request.POST['religion'].upper()
        phone = request.POST['phone']
        blood_group = request.POST['bloodgroup'].upper()
        stage = request.POST['class'].upper()
        address = request.POST['address'].upper()
        disability = request.POST['disability'].upper()
        password = username
        password2 = password

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Student ID Already Exists')
                return redirect('add-student')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
                user.save()
                messages.info(request, 'Student Added Successfully')

                #create a profile object for the new user
                user_model = User.objects.get(username=username, first_name=firstname, last_name=lastname)
                student_profile = Students.objects.create(
                    firstname=firstname, lastname=lastname,
                    user=user_model, password=password,
                    id_user=user_model.id,
                    gender=gender, dob=dob,
                    religion=religion, phone=phone,
                    blood_group=blood_group, stage=stage,
                    address=address, disability=disability)
                student_profile.save()
                return redirect('add-student')

    context = {
        'pagename':pagename,
        'stages':stage
    }
    return render(request, 'lms/add-student.html', context)



@login_required(login_url='admin-login')
def delete_student(request, pk):
    get_user = get_object_or_404(User, username=pk)
    student = get_object_or_404(Students, user=get_user)
    get_user.delete()
    return redirect('students')


@login_required(login_url='admin-login')
def search_student_by_name(request):
    student_name = request.GET.get("name").lower()
    student = Students.objects.filter(lastname__contains=student_name) | Students.objects.filter(firstname__contains=student_name)
    pagename = f"Searched { student_name }"

    allStudents = student.count()

    if allStudents == 0:
        showStudents = "No Student"
    elif allStudents == 1:
        showStudents = f" { allStudents } Student"
    else:
        showStudents = f" { allStudents } Students"

    context = {
        'pagename':pagename,
        'students':student,
        'showStudents':showStudents
    }

    return render(request, 'lms/students.html', context )


#teachers area
@login_required(login_url='admin-login')
def teachers(request):
    pagename = "Teachers"
    teachers = Teachers.objects.all()
    allTeachers = teachers.count()

    if allTeachers == 0:
        showTeachers = "No Teacher"
    elif allTeachers == 1:
        showTeachers = f"{ allTeachers } Teacher"
    else:
        showTeachers = f"{ allTeachers } Teachers"

    context = {
        'pagename':pagename,
        'teachers':teachers,
        'showTeachers':showTeachers
    }
    return render(request, 'lms/teachers.html', context)


@login_required(login_url='admin-login')
def read_teacher(request, pk):
    teacher = Teachers.objects.get(tid=pk)
    pagename = "Teacher"

    context = {
        'pagename':pagename,
        'teacher':teacher
    }
    return render(request, 'lms/index.html', context)


@login_required(login_url='admin-login')
def edit_teacher(request, pk):
    pagename = "Edit Teacher Information"

    teacher = Teachers.objects.get(tid=pk)
    subject = Subjects.objects.all()
    stage = Stages.objects.all()

    if request.method == "POST":
        tid = request.POST['id']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        othername = request.POST['othername']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        disability = request.POST['disability']
        role = request.POST['role']

        teacher.tid = tid
        teacher.lastname = lastname
        teacher.firstname = firstname
        teacher.othername = othername
        teacher.gender = gender
        teacher.phone = phone
        teacher.address = address
        teacher.disability = disability
        teacher.role = role


        teacher.save()
        return redirect('teachers')

    context = {
        'pagename':pagename,
        'teacher':teacher,
        'subjects':subject,
        'stages':stage
    }
    return render(request, 'lms/edit-teacher.html', context)


@login_required(login_url='admin-login')
def add_teacher(request):
    subject = Subjects.objects.all()
    stage = Stages.objects.all()
    pagename = "Add Teacher Information"


    if request.method == "POST":
        tid = request.POST['id']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        othername = request.POST['othername']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        disability = request.POST['disability']
        role = request.POST['role']
        password = tid
        password2 = password


        if password == password2:
            if User.objects.filter(username=tid).exists():
                messages.info(request, 'Teacher ID Already Exists')
                return redirect('add-teacher')
            else:
                user = User.objects.create_user(username=tid, password=password, first_name=firstname, last_name=lastname)

                if role == "Admin":
                    user.is_superuser = True
                    user.is_staff = True
                if role == "Staff":
                    user.is_staff = True
                user.save()

                Teachers.objects.create(
                    tid=tid, lastname=lastname, firstname=firstname,
                    othername=othername, gender=gender, password=password,phone=phone,
                    address=address, disability=disability, role=role)

                messages.info(request, 'Teacher Records Added Successfully')
                return redirect('add-teacher')

    context = {
        'pagename':pagename,
        'subjects':subject,
        'stages':stage
    }

    return render(request, 'lms/add-teacher.html', context)


@login_required(login_url='admin-login')
def delete_teacher(request, pk):
    teacher = Teachers.objects.get(tid=pk)
    teacher.delete()
    return redirect('teachers')


#departments
@login_required(login_url='admin-login')
def departments(request):
    pagename = "Departments"
    department = Departments.objects.all()
    allDepartments = department.count()

    if allDepartments == 0:
        showDepartments = "No Department"
    elif allDepartments == 1:
        showDepartments = f"{ allDepartments } Department"
    else:
        showDepartments = f"{ allDepartments } Departments"

    context = {
        'pagename':pagename,
        'departments':department,
        'showDepartments':showDepartments
    }
    return render(request, 'lms/departments.html', context)


@login_required(login_url='admin-login')
def read_department(request, pk):
    department = Departments.objects.get(did=pk)
    pagename = department

    context = {
        'pagename':pagename,
        'department':department
    }
    return render(request, 'lms/read-department.html', context)


@login_required(login_url='admin-login')
def edit_department(request, pk):
    department = Departments.objects.get(did=pk)
    pagename = department

    if request.method == "POST":
        did = request.POST['id']
        title = request.POST['name']
        hod = request.POST['hod']
        ahod = request.POST['ahod']
        about = request.POST['about']
        staff = request.POST['number']

        department.did = did
        department.title = title
        department.hod = hod
        department.assistant_hod = ahod
        department.about = about
        department.staff = staff

        department.save()
        return redirect('departments')

    context = {
        'pagename':pagename,
        'department':department
    }
    return render(request, 'lms/edit-department.html', context)


@login_required(login_url='admin-login')
def add_department(request):
    pagename = "Add Department Information"

    if request.method == "POST":
        did = request.POST['id']
        title = request.POST['name']
        hod = request.POST['hod']
        ahod = request.POST['ahod']
        about = request.POST['about']
        staff = request.POST['number']

        department = Departments.objects.create(
            did=did, title=title, hod=hod,
            assistant_hod=ahod, about=about,
            number_of_workers=staff)
        department.save()
        messages.info(request, 'Department Records Added Successfully')

    context = {
        'pagename':pagename
    }

    return render(request, 'lms/add-department.html', context)


@login_required(login_url='admin-login')
def delete_department(request, pk):
    department = Departments.objects.get(sid=pk)
    department.delete()
    return redirect('departments')


#subjects area
@login_required(login_url='admin-login')
def subjects(request):
    pagename = "Subjects"
    subjects = Subjects.objects.all()
    allSubjects = subjects.count()

    allSubjects = subjects.count()

    if allSubjects == 0:
        showSubjects = "No Result"
    elif allSubjects == 1:
        showSubjects = f"{ allSubjects } Subject"
    else:
        showSubjects = f"{ allSubjects } Subjects"

    context = {
        'pagename':pagename,
        'subjects':subjects,
        'showSubjects':showSubjects
    }
    return render(request, 'lms/subjects.html', context)


@login_required(login_url='admin-login')
def read_subject(request, pk):
    subject = Subjects.objects.get(code=pk)
    pagename = subject

    context = {
        'pagename':pagename,
        'subject':subject
    }
    return render(request, 'lms/read-subject.html', context)


@login_required(login_url='admin-login')
def edit_subject(request, pk):
    subject = Subjects.objects.get()
    pagename = subject

    context = {
        'pagename':pagename,
        'subject':subject
    }
    return render(request, 'lms/edit-subject.html', context)


@login_required(login_url='admin-login')
def add_subject(request):
    pagename = "Add Subject Information"

    if request.method == "POST":
        sid = request.POST['sid']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        othername = request.POST['othername']
        gender = request.POST['gender']
        dob = request.POST['dob']
        religion = request.POST['religion']
        phone = request.POST['phone']
        blood_group = request.POST['bloodgroup']
        stage = request.POST['class']
        address = request.POST['address']
        disability = request.POST['disability']

        student = Students.objects.create(
            sid=sid, lastname=lastname, firstname=firstname, othername=othername,
            gender=gender, dob=dob, religion=religion, phone=phone,
            blood_group=blood_group, stage=stage,
            address=address, disability=disability)
        student.save()
        messages.info(request, 'Subject Records Added Successfully')

    context = {
        'pagename':pagename
    }

    return render(request, 'lms/add-subject.html', context)


@login_required(login_url='admin-login')
def delete_subject(request, pk):
    subject = Subjects.objects.get(sid=pk)
    subject.delete()
    return redirect('subjects')


@login_required(login_url='admin-login')
def search_subject_by_code(request):
    subject_code = request.GET.get("code")
    subject = Subjects.objects.filter(code__contains=subject_code)
    pagename = f"Searched { subject_code }"

    allSubjects = subject.count()

    if allSubjects == 0:
        showSubjects = "No Result"
    elif allSubjects == 1:
        showSubjects = f"{ allSubjects } Subject"
    else:
        showSubjects = f"{ allSubjects } Subjects"

    context = {
        'pagename':pagename,
        'subjects':subject,
        'showSubjects':showSubjects
    }

    return render(request, 'lms/subjects.html', context )


#accounts
@login_required(login_url='admin-login')
def fees(request):
    pagename = "Fees"
    fees = Fees.objects.all()

    context = {
        'pagename':pagename,
        'fees':fees
    }
    return render(request, 'lms/fees.html', context)


@login_required(login_url='admin-login')
def search_fees_by_student_id(request):
    student_id = request.GET.get("fid")
    fee = Fees.objects.filter(fid__contains=student_id)
    pagename = f"Searched { student_id }"

    allStudents = fee.count()

    if allStudents == 0:
        showStudents = "No Fee"
    elif allStudents == 1:
        showStudents = f" { allStudents } Fee"
    else:
        showStudents = f" { allStudents } Fees"

    context = {
        'pagename':pagename,
        'fees':fee,
        'showStudents':showStudents
    }

    return render(request, 'lms/fees.html', context )


@login_required(login_url='admin-login')
def add_fee(request):
    pagename = "Add Fee"
    term = Terms.objects.all()
    stage = Stages.objects.all()

    if request.method == "POST":
        fid = request.POST['fid']
        stage = request.POST['class']
        term = request.POST['term']
        fee = request.POST['fee']
        amount = request.POST['amount']

        fee = Fees.objects.create(
            fid=fid, stage=stage,
            term=term, amount=amount,
            fee=fee)
        fee.save()
        messages.info(request, 'Fees Records Added Successfully')

    context = {
        'pagename':pagename,
        'stages':stage,
        'terms':term
    }
    return render(request, 'lms/add-fees.html', context)


@login_required(login_url='admin-login')
def edit_fee(request, pk):
    fee = Fees.objects.get(fid=pk)
    pagename = f"Edit Fees { fee.fid }"

    stage = Stages.objects.all()
    term = Terms.objects.all()

    if request.method == "POST":
        fid = request.POST['fid']
        fee = request.POST['fee']
        term = request.POST['term']
        stage = request.POST['class']
        amount = request.POST['amount']

        fee.fid = fid
        fee.fee = fee
        fee.stage = stage
        fee.term = term
        fee.amount = amount
        fee.save()
        return redirect('fees')

    context = {
        'pagename':pagename,
        'fee':fee,
        'terms':term,
        'stages':stage
    }
    return render(request, 'lms/edit-fees.html', context)


@login_required(login_url='admin-login')
def delete_fee(request, pk):
    fee = Fees.objects.get(fid=pk)
    fee.delete()
    return redirect('fees')


#Fees Collection
@login_required(login_url='admin-login')
def fees_collection(request):
    pagename = "Fees Collection"

    fees = FeeCollections.objects.all()

    context = {
        'pagename':pagename,
        'fees':fees
    }
    return render(request, 'lms/fees-collections.html', context)


@login_required(login_url='admin-login')
def add_fees_collection(request):
    pagename = "Add Fees Collection"
    fees = Fees.objects.all()

    if request.method == "POST":
        sid = request.POST['sid']
        amount = request.POST['amount']
        fee = request.POST['fee']
        paid = request.POST['paid']
        arrears = float(amount) - float(paid)
        credit = float(paid) - float(amount)

        if arrears < 0:
            arrears = 0

        if credit < 0:
            credit = 0

        fee_collection = FeeCollections.objects.create(
            sid=sid, amount=amount, fee=fee, paid=paid,
            arrears=arrears, credit=credit
        )
        fee_collection.save()
        messages.info(request, 'Fee Collection Records Added Successfully')

    context = {
        'pagename':pagename,
        'fees':fees
    }
    return render(request, 'lms/add-fees-collection.html', context)


@login_required(login_url='admin-login')
def edit_fee_collection(request, pk):
    fee_collection = FeeCollections.objects.get(sid=pk)
    pagename = f"Edit Fee Collection"

    if request.method == "POST":
        sid = request.POST['sid']
        amount = request.POST['amount']
        fee = request.POST['fee']
        paid = request.POST['paid']
        arrears = float(amount) - float(paid)
        credit = float(paid) - float(amount)

        if arrears < 0:
            arrears = 0

        if credit < 0:
            credit = 0

        fee_collection.sid = sid
        fee_collection.amount = amount
        fee_collection.fee = fee
        fee_collection.paid = paid
        fee_collection.arrears = arrears
        fee_collection.credit = credit
        fee_collection.save()

        return redirect('fees-collection')

    context = {
        'pagename': pagename,
        'fee_collection':fee_collection
    }
    return render(request, 'lms/edit-fee-collection.html', context)


@login_required(login_url='admin-login')
def delete_fee_collection(request, pk):
    fee_collection = FeeCollections.objects.filter(sid=pk)
    fee_collection.delete()
    return redirect('fees-collection')



#Announcements
@login_required(login_url='admin-login')
def announcements(request):
    pagename = "Announcements"

    announcement = Announcement.objects.all()

    context = {
        'pagename':pagename,
        'announcements':announcement
    }
    return render(request, 'lms/announcement.html', context)


@login_required(login_url='admin-login')
def edit_announcement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    pagename = announcement

    context = {
        'pagename':pagename,
        'announcement':announcement
    }
    return render(request, 'lms/edit-announcement.html', context)


@login_required(login_url='admin-login')
def add_announcement(request):
    pagename = "Add Announcement"

    if request.method == "POST":
        heading = request.POST['heading']
        body = request.POST['body']

        announcement = Announcement.objects.create(
            heading=heading, body=body)
        announcement.save()
        messages.info(request, 'Announcement Added Successfully')

    context = {
        'pagename':pagename
    }

    return render(request, 'lms/add-announcement.html', context)


@login_required(login_url='admin-login')
def delete_announcement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    announcement.delete()
    return redirect('announcements')



#Time Table
@login_required(login_url='admin-login')
def time_table(request):
    pagename = "Time Table"
    time_table = TimeTable.objects.all()

    context = {
        'pagename':pagename,
        'time_tables':time_table
    }
    return render(request, 'lms/time-table.html', context)


@login_required(login_url='admin-login')
def add_time_table(request):
    pagename = "Add Time Table"
    subject = Subjects.objects.all()
    stage = Stages.objects.all()
    teacher = Teachers.objects.all()

    if request.method == "POST":
        subject = request.POST['subject']
        day = request.POST['day']
        teacher = request.POST['teacher']
        stage = request.POST['class']
        start = request.POST['start']
        end = request.POST['end']

        time_table = TimeTable.objects.create(
            subject=subject, day=day,
            teacher=teacher, stage=stage,
            start=start, end=end
        )
        time_table.save()
        messages.info(request, 'Time Table Records Added Successfully')

    context = {
        'pagename':pagename,
        'subjcts':subject,
        'stages':stage,
        'teachers':teacher
    }
    return render(request, 'lms/add-time-table.html', context)


#results area
@login_required(login_url='admin-login')
def results(request):
    pagename = "Academic Records"
    result = Result.objects.all()
    allResults = result.count()

    if allResults == 0:
        showResults = "No Result"
    elif allResults == 1:
        showResults = f"{ allResults } Result"
    else:
        showResults = f"{ allResults } Results"


    context = {
        'pagename':pagename,
        'results':result,
        'showResults':showResults
    }
    return render(request, 'lms/results.html', context)


@login_required(login_url='admin-login')
def read_result(request, pk):
    result = Result.objects.get(id=pk)
    pagename = f"Results | { result.sid }"

    context = {
        'pagename':pagename,
        'results':result
    }
    return render(request, 'lms/read-result.html', context)


@login_required(login_url='admin-login')
def edit_result(request, pk):
    result = Result.objects.get(id=pk)
    pagename = f"Edit Results | { result.sid }"

    if request.method == "POST":
        sid = request.POST['sid']
        term = request.POST['term']
        stage = request.POST['class']
        added_by = request.POST['term']
        report = request.FILES.get('report')

        if result.report is not None:
            result.sid=sid
            result.term=term
            result.stage=stage
            result.added_by=added_by
            result.report=result.report
        else:
            result.sid=sid
            result.term=term
            result.stage=stage
            result.added_by=added_by
            result.report=report

        result.save()
        return redirect('results')


    context = {
        'pagename':pagename,
        'result':result,
    }
    return render(request, 'lms/edit-result.html', context)

@login_required(login_url='admin-login')
def delete_result(request, pk):
    result = Result.objects.get(id=pk)
    result.delete()
    return redirect('results')


@login_required(login_url='admin-login')
def search_result_by_id(request):
    result_id = request.GET.get("sid")
    result = Result.objects.filter(sid__contains=result_id)
    pagename = f"Searched { result_id }"

    allResults = result.count()

    if allResults == 0:
        showResults = "No Result"
    elif allResults == 1:
        showResults = f"{ allResults } Result"
    else:
        showResults = f"{ allResults } Results"

    context = {
        'pagename':pagename,
        'results':result,
        'showResults':showResults
    }

    return render(request, 'lms/results.html', context )


#Settings
@login_required(login_url='admin-login')
def settings(request):
    pagename = "Settings"
    site_logo = Logo.objects.first()
    about = About.objects.first()
    contact = Contact.objects.first()
    if request.method == "POST":
        logo = request.FILES.get('logo')

        contact_one = request.POST['contact1']
        contact_two = request.POST['contact2']
        contact_three = request.POST['contact3']

        image = request.FILES.get('image')
        title = request.POST['title']
        mission = request.POST['mission']
        vision = request.POST['vision']
        about = request.POST['about']


        site_logo = Logo.objects.create(
            logo=logo
        )

        contact_details = Contact.objects.create(
            contact_one=contact_one,
            contact_two=contact_two,
            contact_three=contact_three,
        )

        about_us = About.objects.create(
            title=title, mission=mission,
            vision=vision, about=about,
            image=image
        )

        about_us.save()
        site_logo.save()
        contact_details.save()
        messages.success(request, "Contact Details Updated")

    context = {
        'pagename':pagename,
        'logo':site_logo,
        'about':about,
        'contact':contact
    }
    return render(request, 'lms/settings.html', context)


def gallery(request):
    pagename = "Gallery"
    gallery = Gallery.objects.all()

    context = {
        'gallery':gallery
    }
    return render(request, 'lms/gallery.html', context)





@login_required(login_url='staff-login')
def staff_dashboard(request):
    staff = get_object_or_404(User, username=request.user.username)
    attendance = TeacherAttendances.objects.all()
    allAttendance = attendance.count()
    results = Result.objects.filter(added_by=staff)
    allResults = results.count()
    time_table = TimeTable.objects.all()


    teachers = Teachers.objects.all()
    allTeachers = teachers.count()

    if allTeachers == 0:
        showTeachers = "No Teacher"
    elif allTeachers == 1:
        showTeachers = f" { allTeachers } Teacher"
    else:
        showTeachers = f" { allTeachers } Teachers"

    pagename = f"Staff { staff }"

    if allAttendance == 0:
        showAttendance = "No Attendance"
    else:
        showAttendance = f"{ allAttendance } Attendance"

    subjects = Subjects.objects.all()
    allSubjects = subjects.count()

    if allSubjects == 0:
        showSubjects = "No Subject"
    elif allSubjects == 1:
        showSubjects = f" { allSubjects } Subject"
    else:
        showSubjects = f" { allSubjects } Subjects"


    if allResults == 0:
        showResults = "No Result Uploaded"
    elif allResults == 1:
        showResults = f"Uploaded { allResults } Result"
    else:
        showResults = f"Uploaded { allResults } Results"


    context = {
        'pagename':pagename,
        'staff':staff,
        'attendance':attendance,
        'showAttendance':showAttendance,
        'showResults':showResults,
        'results':results,
        'showTeachers':showTeachers,
        'showSubjects':showSubjects
    }
    return render(request, 'lms/teacher-dashboard.html', context)


def teacher_attendance(request):
    return render(request, 'lms/teacher-attendance.html')




@login_required(login_url='student-login')
def student_dashboard(request, pk):
    student = get_object_or_404(User, username=pk)
    student_profile = get_object_or_404(Students, user=student)
    result = Result.objects.filter(sid=student.username)

    pagename = f"Student { student }"
    context = {
        'pagename':pagename,
        'student':student,
        'student_profile':student_profile,
        'results':result
    }
    return render(request, 'lms/student-dashboard.html', context)


def inbox(request):
    pagename = "Message Inbox"
    inbox = Inbox.objects.all()
    allInbox = inbox.count()

    context = {
        'pagename':pagename,
        'inbox':inbox,
        'allInbox':allInbox
    }
    return render(request, 'lms/inbox.html', context)


def compose(request):
    pagename = "Compose Message"
    inbox = Inbox.objects.all()
    allInbox = inbox.count()

    context = {
        'pagename':pagename,
        'allInbox':allInbox
    }
    return render(request, 'lms/compose.html', context)


@login_required(login_url='admin-login')
def add_bulk_students(request):
    pagename = "Add Bulk Students"
    stage = Stages.objects.all()
    message = None
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)
        import csv
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = str(row.get('sid', '')).strip()
                    lastname = str(row.get('lastname', '')).strip().upper()
                    firstname = str(row.get('firstname', '')).strip().upper()
                    gender = str(row.get('gender', '')).strip().upper()
                    dob = str(row.get('dob', '')).strip()
                    religion = str(row.get('religion', '')).strip().upper()
                    phone = str(row.get('phone', ''))
                    blood_group = str(row.get('blood_group', '')).strip().upper()
                    stage_val = str(row.get('stage', '')).strip().upper()
                    address = str(row.get('address', '')).strip().upper()
                    disability = str(row.get('disability', '')).strip().upper()
                    password = username
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
                        user.save()
                        Students.objects.create(
                            firstname=firstname, lastname=lastname,
                            user=user, password=password,
                            id_user=user.id,
                            gender=gender, dob=dob,
                            religion=religion, phone=phone,
                            blood_group=blood_group, stage=stage_val,
                            address=address, disability=disability)
            message = 'Bulk students added successfully.'
        except Exception as e:
            message = f'Error processing file: {e}'
        fs.delete(filename)
    context = {
        'pagename': pagename,
        'stages': stage,
        'message': message
    }
    return render(request, 'lms/add-bulk-students.html', context)


@login_required(login_url='admin-login')
def add_single_result(request):
    pagename = "Add Single Result"
    message = None
    if request.method == "POST":
        sid = request.POST.get('sid')
        stage = request.POST.get('stage')
        name = request.POST.get('name')
        position = request.POST.get('position')
        promoted_to = request.POST.get('promoted_to')
        term = request.POST.get('term')
        number_on_roll = request.POST.get('number_on_roll')
        boys = request.POST.get('boys')
        girls = request.POST.get('girls')
        attendance = request.POST.get('attendance')
        teachers_comment = request.POST.get('teachers_comment')
        next_term = request.POST.get('next_term')
        subject = request.POST.get('subject')
        class_score = request.POST.get('class_score')
        exam_score = request.POST.get('exam_score')
        try:
            result = Result.objects.create(
                sid=sid,
                stage=stage,
                name=name,
                position=position,
                promoted_to=promoted_to,
                term=term,
                number_on_roll=number_on_roll or 0,
                boys=boys or 0,
                girls=girls or 0,
                attendance=attendance,
                teachers_comment=teachers_comment,
                next_term=next_term,
                subject=subject,
                class_score=float(class_score or 0),
                exam_score=float(exam_score or 0),
            )
            result.save()
            message = 'Result added successfully.'
        except Exception as e:
            message = f'Error adding result: {e}'
    context = {
        'pagename': pagename,
        'message': message
    }
    return render(request, 'lms/add-single-result.html', context)


@login_required(login_url='admin-login')
def add_result(request):
    pagename = "Add Bulk Results"
    message = None
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)
        import csv
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sid = str(row.get('sid', '')).strip()
                    stage = str(row.get('stage', '')).strip()
                    name = str(row.get('name', '')).strip()
                    position = str(row.get('position', '')).strip()
                    promoted_to = str(row.get('promoted_to', '')).strip()
                    term = str(row.get('term', '')).strip()
                    number_on_roll = int(row.get('number_on_roll', 0) or 0)
                    boys = int(row.get('boys', 0) or 0)
                    girls = int(row.get('girls', 0) or 0)
                    attendance = str(row.get('attendance', '')).strip()
                    teachers_comment = str(row.get('teachers_comment', '')).strip()
                    next_term = str(row.get('next_term', '')).strip()
                    subject = str(row.get('subject', '')).strip()
                    class_score = float(row.get('class_score', 0) or 0)
                    exam_score = float(row.get('exam_score', 0) or 0)
                    try:
                        Result.objects.create(
                            sid=sid,
                            stage=stage,
                            name=name,
                            position=position,
                            promoted_to=promoted_to,
                            term=term,
                            number_on_roll=number_on_roll,
                            boys=boys,
                            girls=girls,
                            attendance=attendance,
                            teachers_comment=teachers_comment,
                            next_term=next_term,
                            subject=subject,
                            class_score=class_score,
                            exam_score=exam_score
                        )
                    except Exception as e:
                        continue
            message = 'Bulk results added successfully.'
        except Exception as e:
            message = f'Error processing file: {e}'
        fs.delete(filename)
    context = {
        'pagename': pagename,
        'message': message
    }
    return render(request, 'lms/add-bulk-results.html', context)


@login_required(login_url='admin-login')
def download_result_pdf(request, pk):
    result = Result.objects.get(id=pk)
    pagename = f"Results | { result.sid }"
    context = {
        'pagename': pagename,
        'results': result
    }
    html = render_to_string('lms/result-pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="result_{result.sid}_{result.id}.pdf"'
    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode('utf-8')), dest=response, encoding='utf-8'
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


