# Generated by Django 4.0.3 on 2022-04-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_viedo_lectures_subjects_classes_and_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes_and_subjects',
            name='classtype',
            field=models.CharField(default='Not Provided', max_length=30),
        ),
    ]