from django.shortcuts import render
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    logo = Logo.objects.last()
    about_us = About.objects.last()
    hero = Hero.objects.all()
    gallery = Gallery.objects.all()
    programs = Programs.objects.all()
    offer = Offers.objects.all()
    staff = Staff.objects.all()
    blogs = Blogs.objects.all()[:2]
    gallery = Gallery.objects.all()
    contact_details = Contact.objects.last()
    activity = Activities.objects.all()
    pagename = "Home"

    context = {
        'pagename':pagename,
        'logo':logo,
        'about_us':about_us,
        'hero':hero,
        'gallery':gallery,
        'programs':programs,
        'offers':offer,
        'staff':staff,
        'blogs':blogs,
        'gallery':gallery,
        'contact_details':contact_details,
        'activities':activity
    }
    return render(request, 'index.html', context)



def about(request):
    logo = Logo.objects.last()
    about_us = About.objects.last()
    staff = Staff.objects.all()
    gallery = Gallery.objects.all()
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    pagename = "About Us"

    context = {
        'pagename':pagename,
        'logo':logo,
        'about_us':about_us,
        'staff':staff,
        'gallery':gallery,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'about.html', context)



def activities(request):
    logo = Logo.objects.last()
    gallery = Gallery.objects.all()
    activity = Activities.objects.all()
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    
    pagename = "Activities"

    context = {
        'pagename':pagename,
        'logo':logo,
        'gallery':gallery,
        'activities':activity,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'activities.html', context)


def activity_details(request, slug):
    logo = Logo.objects.last()
    gallery = Gallery.objects.all()
    activity = Activities.objects.get(slug=slug)
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    pagename = "Activity Details"

    context = {
        'pagename':pagename,
        'logo':logo,
        'gallery':gallery,
        'activity':activity,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'activity-details.html', context)


def blog_details(request, slug):
    logo = Logo.objects.last()
    gallery = Gallery.objects.all()
    blog = Blogs.objects.get(slug=slug)
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    pagename = "Blog Details"

    context = {
        'pagename':pagename,
        'logo':logo,
        'gallery':gallery,
        'blog':blog,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'blogs-details.html', context)


def blogs(request):
    logo = Logo.objects.last()
    blogs = Blogs.objects.all()
    gallery = Gallery.objects.all()
    contact_details = Contact.objects.last()
    pagename = "Blogs"

    context = {
        'pagename':pagename,
        'logo':logo,
        'blogs':blogs,
        'gallery':gallery,
        'contact_details':contact_details
    }
    return render(request, 'blogs.html', context)



def gallery(request):
    logo = Logo.objects.last()
    contact_details = Contact.objects.last()
    pagename = "Gallery"

    context = {
        'pagename':pagename,
        'logo':logo,
        'contact_details':contact_details
    }
    return render(request, 'index.html', context)


def admissions(request):
    logo = Logo.objects.last()
    contact_details = Contact.objects.last()
    pagename = "Admissions"

    context = {
        'pagename':pagename,
        'logo':logo,
        'contact_details':contact_details
    }
    return render(request, 'index.html', context)


def faculty(request):
    logo = Logo.objects.last()
    staff = Staff.objects.all()
    gallery = Gallery.objects.all()
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    pagename = "Faculty"

    context = {
        'pagename':pagename,
        'logo':logo,
        'staff':staff,
        'gallery':gallery,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'faculty.html', context)


def contact(request):
    logo = Logo.objects.last()
    gallery = Gallery.objects.all()
    contact_details = Contact.objects.last()
    blogs = Blogs.objects.all()
    pagename = "Contact"

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Inbox.objects.create(
            name = name, email = email, message = message
        )
        messages.success(request, "Message Submitted")

    context = {
        'pagename':pagename,
        'logo':logo,
        'gallery':gallery,
        'blogs':blogs,
        'contact_details':contact_details
    }
    return render(request, 'contact.html', context)

