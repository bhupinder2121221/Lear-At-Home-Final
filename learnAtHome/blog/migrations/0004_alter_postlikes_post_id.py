# Generated by Django 4.0.3 on 2022-03-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_postlikes_nooflikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlikes',
            name='post_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]