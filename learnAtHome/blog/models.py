
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, fname, password=None, **otherFields):
        if not email:
            raise ValueError("Email must be defiend")
        email = self.normalize_email(email)
        user = self.model(email=email, fname=fname, **otherFields)
        user.set_password(password)
        user.save()

    def create_superuser(self, email, fname, password=None, **otherFields):
        otherFields.setdefault('is_staff', True)
        otherFields.setdefault('is_superuser', True)
        if otherFields.get('is_staff') != True and otherFields.get('is_superuser') != True:
            raise ValueError("is staff , is_superuser is False in SuperUser")

        return self.create_user(email, fname, password, **otherFields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField('FirstName', max_length=15, blank=False)
    lname = models.CharField('LastName', max_length=15, blank=True)
    email = models.CharField('Email', max_length=30, primary_key=True)
    dob = models.DateField('DOB', blank=True, null=True)
    is_staff = models.BooleanField('IsStaff', default=False)
    is_superuser = models.BooleanField('IsSuperUser', default=False)
    password = models.CharField('Password', max_length=16, blank=False)
    profile = models.ImageField(
        'ProfileImage', blank=False, upload_to="profile/")

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname']

    def __str__(self):
        return self.fname


class PostLikes(models.Model):
    post_id = models.AutoField(primary_key=True)
    likedBy = models.ManyToManyField(CustomUser)
    NoOfLikes = models.IntegerField('Likes', default=0)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dateTime = models.DateTimeField('DateTime', auto_now_add=True)
    image = models.ImageField('BlogImage', upload_to=f'bolgImages/')
    postlike = models.OneToOneField(
        PostLikes, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title[:20] + " | Author : " + str(self.author)


# Create your models here.
class RegisterFormModel(models.Model):
    fname = models.CharField('FirstName', max_length=15, blank=False)
    lname = models.CharField('LastName', max_length=15, blank=True)
    email = models.CharField('Email', max_length=30, primary_key=True)
    dob = models.DateField('DOB')
    password = models.CharField('Password', max_length=16, blank=False)
    profile = models.ImageField(
        'ProfileImage', blank=False, upload_to="profile/")

    def __str__(self):
        return self.email

# uesr is followed by


class FollowdByModel(models.Model):

    email = models.CharField(max_length=30, primary_key=True)
    follwedBy = models.ManyToManyField(CustomUser)

# user is following


class FolowersModel(models.Model):

    email = models.CharField(max_length=30, primary_key=True)
    followers = models.ManyToManyField(CustomUser)

# for classroom


class viedo_lectures(models.Model):
    title = models.CharField(max_length=100, default="No Title")
    video_url = models.TextField()


class subjects(models.Model):
    subject = models.CharField(max_length=30)
    viedo_lectures = models.ManyToManyField(viedo_lectures)
    image = models.TextField(default="")


class Classes_and_subjects(models.Model):
    myclass = models.CharField(max_length=20)
    classtype = models.CharField(max_length=30, default="Not Provided")
    subject = models.ManyToManyField(subjects)
    picture = models.ImageField('bannerpic', upload_to="banners/", default="")

    def __str__(self) -> str:
        return self.myclass


class Sellers(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField()
    shopname = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name + " | " + str(self.shopname)


class StoreItems(models.Model):
    title = models.CharField(max_length=100)
    seller = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    price = models.IntegerField()
    classtype = models.CharField(max_length=50, default="")
    noOfItems = models.IntegerField(default=0)
    image = models.TextField()
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title + " | " + str(self.seller.name)


class OrderedItmes(models.Model):
    items = models.ForeignKey(
        StoreItems, on_delete=models.SET_DEFAULT, default="Item  not available")
    datetime = models.CharField(max_length=100)
    totalPrice = models.IntegerField()
    transectionId = models.TextField()
    buyer_email = models.CharField(max_length=50, default="Not Given")
    address = models.TextField(default="No Address Given")

    def __str__(self) -> str:
        return self.items.title + str(" | ") + str(self.transectionId) + " | " + str(self.buyer_email)
