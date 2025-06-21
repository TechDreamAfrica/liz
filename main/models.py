from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class Hero(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='Hero Images')
    date_posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_posted']
        db_table = ''
        managed = True
        verbose_name = 'Hero'
        verbose_name_plural = 'Hero'

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=100)
    mission = RichTextUploadingField()
    vision = RichTextUploadingField()
    image = models.ImageField(upload_to="About Images")
    about = RichTextUploadingField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'About'
        verbose_name_plural = 'About Us'


    def __str__(self):
        return self.title



class Programs(models.Model):
    title = models.CharField(max_length=100)
    age_range = models.CharField(max_length=100)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to="Program Images")

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Programs'
        verbose_name_plural = 'Programs'


    def __str__(self):
        return self.title


class Offers(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Offers'
        verbose_name_plural = 'Offers'


    def __str__(self):
        return self.title
    


class Activities(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='Activity Images')
    date_added = models.DateTimeField(auto_created=True, auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['-date_added']
        unique_together = ('title', 'date_added')
        db_table = ''
        managed = True
        verbose_name = 'Activities'
        verbose_name_plural = 'Activities'

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Activities, self).save(*args, **kwargs)


    def __str__(self):
        return self.title
    


class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    about = RichTextUploadingField()
    image = models.ImageField(upload_to='executive_images')
    date_posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_posted']
        db_table = ''
        managed = True
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'


    def __str__(self):
        return f"Staff {self.name}"



class Blogs(models.Model):
    headline = models.CharField(max_length=200)
    posted_by = models.CharField(max_length=20, default="Admin")
    date_posted = models.DateTimeField(default=timezone.now)
    article = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_images')
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["-date_posted"]
        unique_together = ('headline', 'date_posted')
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.headline)
        super(Blogs, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline


class Announcement(models.Model):
    heading = models.CharField(max_length=200)
    body = RichTextUploadingField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        db_table = ''
        managed = True
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.heading



class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery_images')
    date_posted = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-date_posted']
        db_table = ''
        managed = True
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.title


class Inbox(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = RichTextUploadingField()
    date_posted = models.DateTimeField(auto_now=True)

    class Mata:
        ordering = ['-date_posted']
        db_table = ''
        managed = True
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


    def __str__(self):
        return f'Message from {self.name}'


class Contact(models.Model):
    primary_contact = models.CharField(max_length=20)
    secondary_contact = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Contact Detail'
        verbose_name_plural = 'Contact Details'


    def __str__(self):
        return 'Contact Details'


class Logo(models.Model):
    logo = models.ImageField(upload_to='school_logo')

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'


    def __str__(self):
        return 'School Logo'
