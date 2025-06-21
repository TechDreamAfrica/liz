from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('about', views.about, name='about'),
    path('activities', views.activities, name='activities'),
    path('blogs', views.blogs, name='blogs'),
    path('activities', views.activities, name='activities'),
    path('contact', views.contact, name='contact'),
    path('faculty', views.faculty, name='faculty'),

    path('activity-details/<str:slug>', views.activity_details, name='activity-details'),
    path('blogs/<str:slug>', views.blog_details, name='blog-details'),
]