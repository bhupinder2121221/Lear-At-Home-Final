# Generated by Django 4.0.3 on 2022-03-31 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_followdbymodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='bolgImages/', verbose_name='BlogImage'),
        ),
    ]
