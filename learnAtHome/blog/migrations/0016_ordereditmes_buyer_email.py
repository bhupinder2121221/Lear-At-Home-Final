# Generated by Django 4.0.3 on 2022-04-30 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_sellers_storeitems_ordereditmes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditmes',
            name='buyer_email',
            field=models.CharField(default='Not Given', max_length=50),
        ),
    ]
