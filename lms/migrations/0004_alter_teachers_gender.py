# Generated by Django 5.1.3 on 2025-06-11 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_remove_teachers_blood_group_remove_teachers_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
