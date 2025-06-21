from django.urls import path
from .auth_view import *
from .admin_view import *

urlpatterns = [
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),


    path('index/', index, name='admin-homepage'),

    path('students', students, name='students'),
    path('students/read-student/<str:pk>', read_student, name='read-student'),
    path('students/add-student/', add_student, name='add-student'),
    path('students/delete-student/<str:pk>', delete_student, name='delete-student'),
    path('students/edit-student/<str:pk>', edit_student, name='edit-student'),


    path('results', results, name='results'),
    path('results/read-result/<str:pk>', read_result, name='read-result'),
    path('results/add-result', add_result, name='add-result'),
    path('results/edit-result/<str:pk>', edit_result, name='edit-result'),
    path('results/delete-result/<str:pk>', delete_result, name='delete-result'),

    path('teachers', teachers, name='teachers'),

    # path('settings', settings, name='settings'),

    path('staff/staff-dashboard/', staff_dashboard, name='staff-dashboard'),
    
    path('teachers/read-teacher/<str:pk>', read_teacher, name='read-teacher'),
    path('teachers/add-teacher', add_teacher, name='add-teacher'),
    path('teachers/edit-teacher/<str:pk>', edit_teacher, name='edit-teacher'),
    path('teachers/delete-teacher/<str:pk>', delete_teacher, name='delete-teacher'),
    
    
    path('departments', departments, name='departments'),
    path('departments/read-department/<str:pk>', read_department, name='read-department'),
    path('departments/add-department', add_department, name='add-department'),
    path('departments/edit-department/<str:pk>', edit_department, name='edit-department'),
    path('departments/delete-department/<str:pk>', delete_department, name='delete-department'),
    
    path('subjects', subjects, name='subjects'),
    path('subjects/read-subject/<str:pk>', read_subject, name='read-subject'),
    path('subjects/add-subject', add_subject, name='add-subject'),
    path('subjects/edit-subject/<str:pk>', edit_subject, name='edit-subject'),
    path('subjects/delete-subject/<str:pk>', delete_subject, name='delete-subject'),
    
    path('fees', fees, name='fees'),
    path('fees/add-fee', add_fee, name='add-fee'),
    path('fees/delete-fee/<str:pk>', add_fee, name='delete-fee'),
    path('fees/edit-fee/<str:pk>', edit_fee, name='edit-fee'),
    
    path('fees-collection', fees_collection, name='fees-collection'),
    path('add-fees-collection', add_fees_collection, name='add-fees-collection'),
    path('edit-fee-collection/<str:pk>', edit_fee_collection, name='edit-fee-collection'),
    path('delete-fee-collection/<str:pk>', delete_fee_collection, name='delete-fee-collection'),
    
    #Time Table
    path('time-table', time_table, name='time-table'),
    path('add-time-table', add_time_table, name='add-time-table'),

    #search
    path('search-student-by-name/', search_student_by_name, name='search-student-by-name'),
    path('search-result-by-id/', search_result_by_id, name='search-result-by-id'),
    path('search-fees-by-student-id/', search_fees_by_student_id, name='search-fees-by-student-id'),
    path('search-subject-by-code/', search_subject_by_code, name='search-subject-by-code'),
    
    #Announcement
    path('announcements', announcements, name='announcements'),
    path('announcements/add-announcement', add_announcement, name='add-announcement'),
    path('announcements/edit-announcement/<str:pk>', edit_announcement, name='edit-announcement'),
    path('announcements/delete-announcement/<str:pk>', delete_announcement, name='delete-announcement'),
    
    #Teachers
    path('teachers/read-teacher/<int:tid>', read_teacher, name='read-teacher'),
    path('teachers/add-teacher', add_teacher, name='add-teacher'),
    path('teachers/edit-teacher/<int:tid>', edit_teacher, name='edit-teacher'),
    path('teachers/delete-teacher/<int:tid>', delete_teacher, name='delete-teacher'),
    

    #Messages
    path('inbox', inbox, name='inbox'),
    path('compose', compose, name='compose'),
    
]
