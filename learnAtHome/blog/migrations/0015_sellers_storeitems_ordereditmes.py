# Generated by Django 4.0.3 on 2022-04-30 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_remove_subjects_picture_subjects_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('shopname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StoreItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('noOfItems', models.IntegerField(default=0)),
                ('image', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.sellers')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedItmes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=100)),
                ('totalPrice', models.IntegerField()),
                ('transectionId', models.TextField()),
                ('address', models.TextField()),
                ('items', models.ForeignKey(default='Item  not available', on_delete=django.db.models.deletion.SET_DEFAULT, to='blog.storeitems')),
                ('seller', models.ForeignKey(default='seller is not available', on_delete=django.db.models.deletion.SET_DEFAULT, to='blog.sellers')),
            ],
        ),
    ]