# ^^^^^^^^^^^^^ Error in sending blog image in json file
# paytm imports ------------------------------------
from distutils.log import Log
from .models import StoreItems, OrderedItmes, Sellers
from django.forms import EmailInput
from paytmchecksum import PaytmChecksum
import string
import numpy
from django.views.decorators.csrf import csrf_exempt
# ------------------------------------------------------

from django.shortcuts import render, redirect
from django.urls import reverse
from blog.forms import form
from django.http import HttpResponse
from blog.customForm import LoginForm, RegisterForm, PostForm, addSubject, addClass, addLecture, addItemForm
from django.core.files.storage import FileSystemStorage
from .models import RegisterFormModel, CustomUser
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from pytz import timezone
from .models import CustomUser, PostLikes, Post, FollowdByModel, FolowersModel
import requests
import json
from getpass import getpass  # for getting password
paytm_id = "YuCIKo79275916814234"
paytm_key = "Mpb_YIN4h5kwMKfY"


def encrypt(s):
    return s


def decrypt(s):
    return s


def getToken(request, username, password):

    endpoint = 'http://127.0.0.1:8000/api/gettoken/'
    auth_response = requests.post(
        endpoint, data={'username': username, 'password': password})
    if auth_response.status_code == 200:
        print(auth_response.json()['token'])
        request.session['token'] = auth_response.json()['token']
    else:
        return HttpResponse("Cannot genertate token")


def getdetailOfProfile(username):
    print(username)
    followersNo = 0
    followingNo = 0
    likesNo = 0
    followingNo = len(FolowersModel.objects.get(
        email=username).followers.all())
    for obj in FollowdByModel.objects.all():
        for obj1 in obj.follwedBy.all():
            if obj1.email == username:
                followersNo += 1
    for obj in Post.objects.all():
        # print(obj.author.email)
        if obj.author.email == username:
            likesNo += obj.postlike.NoOfLikes
    return {
        'likes': likesNo,
        'followers': followersNo,
        'following': followingNo
    }


def get_Profiledata(request):
    profile_endpoint = "http://127.0.0.1:8000/api/profile/"
    profile_response = requests.get(profile_endpoint, headers={
        'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={"username": request.user.email})
    aditional_data = getdetailOfProfile(
        profile_response.json()['email'])
    return profile_response, aditional_data


def get_friend_list(request):
    friendlist_endpoint = 'http://127.0.0.1:8000/api/friendlist/'
    friendlist_response = requests.post(friendlist_endpoint, headers={
                                        'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={"username": request.user.email})
    return friendlist_response


def set_testCookie(request):
    """This function will check the compatublity of browser for cookies and session"""
    request.session.set_test_cookie()


def check_set_testCookie(request):
    """This function sees if browser was able to store test cookie"""
    if request.session.test_cookie_worked():
        print("Browser is compatible")
        request.session.delete_test_cookie()
        return True
    else:
        print("The browser is not compatible")
        return False
# ------------------------ Home page ---------------------------------------


@login_required(login_url="/login/", redirect_field_name="redirect_to")
def user_homePage(request, pageno, filter=None):
    urlpath = request.path.split('filter')[0][:-1]
    print(urlpath)
    if 'pageno' in urlpath:
        urlpath.replace('page-'+str(pageno), 'page-1')
    else:
        urlpath = "/page-1"
    filtertag = ""
    filterapplied = ""
    posts = requests.get('http://127.0.0.1:8000/api/')
    profile_endpoint = "http://127.0.0.1:8000/api/profile/"
    profile_response = requests.get(profile_endpoint, headers={
                                    'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={"username": request.user.email})
    aditional_data = getdetailOfProfile(profile_response.json()['email'])
    if filter != None:
        if filter == "desc":
            filtertag = "Newest"
            filterapplied = "filter-desc"
            posts = posts.json()[-1::-1]
        elif filter == 'asc':
            filterapplied = "filter-asc"
            filtertag: "Newest"
            posts = posts.json()
        elif filter == 'myblog':
            filterapplied = "filter-myblog"
            filtertag = "My Blogs"
            posts = posts.json()
            postsArray = []
            for post in posts:
                print(post)
                if post['author'] == request.user.email:
                    postsArray.append(post)
            posts = postsArray
        elif filter == "following":
            filterapplied = "filter-following"
            posts = requests.get('http://127.0.0.1:8000/api/filterFollowers/', headers={
                                 'Authorization': "SecretToken "+str(request.session.get('token'))}).json()
    else:
        filtertag = "Newest"
        posts = posts.json()[-1::-1]

    pages = Paginator(posts, 4)
    # print(posts.json())
    # print(friendlist_response.json().values())
    request.session['profileData'] = profile_response.json()
    request.session['additionalData'] = aditional_data

    nodata = False
    if pageno > pages.num_pages:
        pageno = pages.num_pages
        nodata = True
    print(pageno, "page-------------------")
    certain_page = pages.page(pageno)

    for page in certain_page:
        pl = Post.objects.get(post_id=page['post_id']).postlike.likedBy.all()
        fl = FolowersModel.objects.get(
            email=request.user.email).followers.all()
        print("All followers of user ", request.user.email, "  are : ", fl)
        found = False
        isMyPost = False
        for follower in fl:
            if page['author'] == follower.email:
                found = True

                print("You are following")
                break

        if page['author'] == request.user.email:
            isMyPost = True
        page['content'] = page['content'][:40]
        page['isMyPost'] = isMyPost
        page['dateTime'] = datetime.fromisoformat(
            page['dateTime'].split('.')[0])
        if found:
            page['following'] = True
        else:
            page['following'] = False

        if len(pl.filter(email=request.user.email)):
            # print("You Liked this page")
            page['liked'] = True
        else:
            # print("You didn't liked this page")
            page['liked'] = False
        # print(pl)
        # print(pl.filter(email=request.user.email))
        print(request.path)
        redirecturlpath = "http://127.0.0.1:8000"+request.path

        context = {
            'posts': certain_page,
            'pageno': pageno,
            'profile': profile_response.json(),
            'otherdata': aditional_data,
            'user': True,
            # 'friendlist': friendlist_response.json(),
            'filterpath': urlpath,
            'filtertag': filtertag,
            'filterapplied': filterapplied,
            'likeredirect': redirecturlpath.replace('/', "&"),
            'nodata': nodata,
            'myfeeds': True,
            'myfeeds': True
        }
        print(context)
    return render(request, 'home.html', context)


def default_homePage(request, pageno, filter=None):
    urlpath = request.path.split('filter')[0][:-1]
    print(urlpath)
    filterapplied = ""
    posts = requests.get('http://127.0.0.1:8000/api/')
    filtertag = ""
    if filter != None:
        if filter == 'desc':
            filterapplied = "filter-desc"
            posts = posts.json()[-1::-1]
            filtertag = "Newest"
        elif filter == 'asc':
            filterapplied = "filter-asc"
            filtertag = "Oldest"
            posts = posts.json()

    else:
        posts = posts.json()[-1::-1]
        filtertag = "Newest"

    pages = Paginator(posts, 4)
    nodata = False
    if pageno > pages.count:
        pageno = pages.num_pages
        nodata = True
    certain_page = pages.page(pageno)

    for page in certain_page:
        page['content'] = page['content'][:40]
        page['liked'] = False
        page['dateTime'] = datetime.fromisoformat(
            page['dateTime'].split('.')[0])
    redirecturlpath = 'http://127.0.0.1:8000' + request.path
    context = {
        'posts': certain_page,
        'pageno': pageno,
        'user': False,
        'friendlist': False,
        'filterpath': urlpath,
        'filtertag': filtertag,
        'nodata': nodata,
        'likeredirect': redirecturlpath.replace('/', '&'),
        'myfeeds': True,
        'myfeeds': True

    }

    return render(request, 'home.html', context)


class friendPostView(LoginRequiredMixin, View):
    redirect_field_name = 'redirect_to'
    login_url = '/login/'

    def get(self, request, pageno, friendEmail, pgnumber=1, filter=None):
        posts = Post.objects.filter(author=friendEmail).all()
        urlpath = request.path.split('filter')[0][:-1]
        print(urlpath)
        filterapplied = ""
        filtertag = ""
        if filter:
            if filter == "desc":
                filterapplied = "filter-desc/"
                filtertag = "Latest"
                posts = posts.order_by('-dateTime')
            elif filter == 'asc':
                filterpath = "filter-asc/"
                posts = posts
                filtertag = "Oldest"

        else:
            posts = posts.order_by('-dateTime')
        pages = Paginator(posts, 5)
        nodata = False
        if pageno > pages.count:
            pageno = pages.num_pages
            nodata = True
        certain_page = pages.page(pageno)
        for page in certain_page:
            page.content = page.content[:40]
            page.dateTime = datetime.fromisoformat(
                str(page.dateTime).split('.')[0])

        aditional_data = getdetailOfProfile(friendEmail)
        profile_response = requests.get('http://127.0.0.1:8000/api/profile/', headers={
                                        'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={'username': friendEmail}).json()
        friendlist_response = get_friend_list(request).json()
        print(aditional_data, profile_response, friendlist_response)
        redirecturlpath = "http://127.0.0.1:8000"+request.path
        context = {
            'posts': certain_page,
            'pageno': pageno,
            'profile': profile_response,
            'otherdata': aditional_data,
            'user': True,
            'myfeeds': True,
            'friendlist': friendlist_response,
            'friendpost': True,
            'filterpath': urlpath,
            'nodata': nodata,
            'filterapplied': filterapplied,
            'filtertag': filtertag,
            'likeredirect': redirecturlpath.replace('/', '&')

        }
        return render(request, 'home.html', context)


@login_required(login_url='/login/', redirect_field_name='redirect_to')
def postlikeView(request, pageno, post_id, redirecturl):
    pl = Post.objects.get(post_id=post_id).postlike
    pl1 = pl.likedBy
    pl2 = pl1.all()
    print("Liking post")
    if len(pl2.filter(email=request.user.email)):
        # remove like
        p = pl2.filter(email=request.user.email)[0]
        pl.NoOfLikes -= 1
        pl1.remove(p)
        print("post unliked")
        pl.save()
    else:
        pl1.add(request.user)
        pl.NoOfLikes += 1
        pl.save()

        print("post liked")
    return redirect(redirecturl.replace("&", "/"))
    # return redirect('/page-'+str(pageno))


@login_required(login_url='/login/', redirect_field_name='redirect_to')
def followedView(request, pageno, SecondEmail, redirecturl):

    endpoint = "http://127.0.0.1:8000/api/user/follower/"
    data = {
        "username": request.user.email,
        "targetUserName": SecondEmail
    }
    token = request.session.get('token')
    response = requests.post(
        endpoint, headers={'Authorization': 'SecretToken '+str(token)}, data=data)
    print("respone from followedapi : ", response)
    # return HttpResponse("Follow page")
    return redirect(redirecturl.replace('&', "/"))


class DeletePostView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request, redirecturl):
        delete_endpoint = "http://127.0.0.1:8000/api/deletepost"
        delete_response = requests.delete(delete_endpoint, headers={'Autho'})
        return redirect(redirecturl.replace("&", "/"))


def homePage(request, pageno=1, filter=None):
    request.session.set_expiry(30000)
    request.session.clear_expired()
    print(request.session.get_expiry_age())
    set_testCookie(request)  # setting test cokkie for compatibility check

    if request.user.is_authenticated:

        return user_homePage(request, pageno, filter)
    else:

        return default_homePage(request, pageno, filter)

# ---------------------------------------------------------------------------


# ------------------------- New post page -------------------------------------
# @login_required(login_url='/login/',redirect_field_name='redirect_to')   -- for function based view
class New_PostPage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        myform = PostForm()
        # resutlt = requests.get("http://localhost:8000/api/")
        context = {
            'form': myform,
            'author': request.user.email,
            'friendpost': True,
            "pageno": 1,
            'otherdata': getdetailOfProfile(request.user.email),
            # 'friendlist': request.session.get('friendListData'),
            'profile': requests.get('http://127.0.0.1:8000/api/profile/', headers={'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={'username': request.user.email}).json()
        }
        return render(request, 'newPost.html', context)

    def post(self, request):
        myform = PostForm(request.POST, request.FILES)
        if myform.is_valid():
            print(myform.cleaned_data['title'])
            datajson = {}
            datajson['title'] = myform.cleaned_data['title']
            datajson['content'] = myform.cleaned_data['content']
            datajson['author'] = request.user.email
            datajson['dateTime'] = datetime.now(timezone('Asia/Kolkata'))
            datajson['image'] = myform.cleaned_data['image']

            resutlt = requests.post("http://localhost:8000/api/user/", headers={
                                    'Authorization': "SecretToken "+str(request.session.get('token'))}, data=datajson)
            print(resutlt.text)

            if resutlt.json()['error'] == 'no error':
                return HttpResponse("Post saved successfully")
            else:
                context = {
                    'form': myform,
                    'error': resutlt.error,
                    "pageno": 1,
                    'friendpost': True,
                    # 'friendlist': request.session.get('friendListData'),
                    'profile': requests.get('http://127.0.0.1:8000/api/profile/', headers={'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={'username': request.user.email}).json(),
                    'otherdata': getdetailOfProfile(request.user.email)
                }
                return render(request, 'newPost.html', context)
            # return HttpResponse("Success")
        else:
            context = {
                'form': myform,
                'friendpost': True,
                "pageno": 1,
                'author': request.user.email,
                # 'friendlist': request.session.get('friendListData'),
                'profile': requests.get('http://127.0.0.1:8000/api/profile/', headers={'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={'username': request.user.email}).json(),
                'otherdata': getdetailOfProfile(request.user.email)

            }
            return render(request, 'newPost.html', context)

# ----------------------------------------------------------------------------


# ---------------------------- Register page -------------------------------
def handleProfileImage(image, name):
    fs = FileSystemStorage()
    fileExtension = image.name.split(".")
    fileExtension = fileExtension[len(fileExtension)-1]
    fileDestination = 'profile/' + name+'.'+fileExtension
    filename = fs.save(fileDestination, image)
    print(filename)
    print("profile pic saved")
    return fileDestination


def register_page(request):
    if request.method == 'POST':
        myform = RegisterForm(request.POST, request.FILES)
        # print(myform.error_messages)
        if myform.is_valid():
            pic = request.FILES['profile']
            print("uploaded file is : ", pic.name)

            pic.name = myform.cleaned_data['email']
            # filedestination = handleProfileImage(pic,myform.cleaned_data.get('email'))
            CustomUser.objects.create_user(
                fname=myform.cleaned_data['fname'],
                lname=myform.cleaned_data['lname'],
                email=myform.cleaned_data['email'],
                dob=myform.cleaned_data['dob'],
                password=myform.cleaned_data['password'],
                profile=myform.cleaned_data['profile'],
                is_staff=False,
                is_superuser=False
            )
            fl = FollowdByModel.objects.create(
                email=myform.cleaned_data['email'])
            fl.save()
            fl = FolowersModel.objects.create(
                email=myform.cleaned_data['email'])
            fl.save()

            return HttpResponse('Success ! databse uploaded')
        return render(request, 'register.html', {'form': myform})
    else:
        myform = RegisterForm()
        context = {
            'form': myform
        }
        return render(request, 'register.html', context)
# --------------------------------------------------------------------------

# -------------------------- LOGIN LOGOUT-----------------------------
# checking login credentials


def checkLoginCredentials(request, email, password):

    user = authenticate(request, username=email, password=password)
    print("user found :", user)
    if user is not None:
        return True, user
    else:
        return False, None


class Login_Page(View):

    def get(self, request):
        # checking browser-cookie compatibilty
        if check_set_testCookie(request):
            # setting redirect url
            request.session["next_url"] = request.GET.get('redirect_to', "/")

            myform = LoginForm(None)
            context = {
                'form': myform
            }
            return render(request, 'login.html', context)
        else:
            return HttpResponse("Your browser is not compatible for cookies. <a href='/'>Retry</a>")

    def post(self, request):

        myform = LoginForm(request.POST)
        context = {
            'form': myform
        }
        if myform.is_valid():
            status, user = checkLoginCredentials(request, myform.cleaned_data.get(
                'email'), myform.cleaned_data.get('password'))
            if status:
                login(request, user)
                nextUrl = request.session.get("next_url", "/")
                getToken(request, myform.cleaned_data.get('email'),
                         myform.cleaned_data.get('password'))
                http = redirect(nextUrl)

                # setting expiration of cookie
                currentTime = datetime.now(timezone('Asia/Kolkata'))
                deadline = currentTime + timedelta(days=7)
                NoOfSeconds = deadline.timestamp() - currentTime.timestamp()
                http.set_cookie("user_id", user.email, NoOfSeconds)
                return http
            else:
                return HttpResponse("Login Wrong credentials")

        else:
            return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    request.session.clear()
    return redirect('/')
# -------------------------------------------------------------------


# -------------- classroom section -----------------
def sortArray(arr1, arr2):
    n = len(arr1)
    for i in range(n):
        for j in range(n-1-i):
            if arr1[j] > arr1[j+1]:
                arr1[j], arr1[j+1] = arr1[j+1], arr1[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]


def get_classNumbers(request):
    endpoint = "http://127.0.0.1:8000/api/classroom"
    response = requests.get(endpoint, headers={
                            'Authorization': 'SecretToken '+str(request.session.get('token'))})

    primaryClasses = {}
    secondaryClasses = {}
    temp = 0
    if response:
        for classobj in response.json():
            if classobj["classtype"] == "primary":
                if classobj["myclass"][5:] == "10":
                    temp = classobj
                else:
                    primaryClasses[int(classobj["myclass"][5:])
                                   ] = classobj['picture']
            else:
                secondaryClasses[int(classobj["myclass"][5:])
                                 ] = classobj['picture']
    primaryClasses[int(temp["myclass"][5:])
                   ] = temp['picture']
    return primaryClasses, secondaryClasses


def add_classNumbers(request, classno, classtype):
    endpoint = "http://127.0.0.1:8000/api/classroom/"
    response = requests.post(endpoint, headers={
        'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={"classno": str(classno), "classtype": classtype.capitalize()})
    print(response)


class ClassroomHome(LoginRequiredMixin, View):  # global view
    login_url = "/login"
    redirect_field_name = 'redirect_to'

    def post(self, request):
        form = addClass(request.POST)
        if form.is_valid():
            add_classNumbers(
                request, form.cleaned_data['className'], form.cleaned_data['classType'])
        return self.get(request)

    def get(self, request):
        # form for adding class
        form = addClass()

        # getting classes data
        classes, secondaryclasses = get_classNumbers(request)

        materials = ['Books', 'Stationary']
        if request.user.is_authenticated:

            profile_endpoint = "http://127.0.0.1:8000/api/profile/"
            profile_response = requests.get(profile_endpoint, headers={
                                            'Authorization': 'SecretToken '+str(request.session.get('token'))}, data={"username": request.user.email})
            aditional_data = getdetailOfProfile(
                profile_response.json()['email'])

            context = {
                'profile': profile_response.json(),
                'otherdata': aditional_data,
                'classes': classes,
                'secondaryclasses': secondaryclasses,
                'materials': materials,
                'classroom': True,
                'form': form,

            }
            if request.user.is_staff:
                context['superUser':True]
            return render(request, 'classroom.html', context)
        else:
            context = {
                'user': False,
                'classes': classes,
                'secondaryclasses': secondaryclasses,
                'materials': materials,
                'classroom': True
            }
            if request.user.is_staff:
                context['superUser':True]
            return render(request, 'classroom.html', context)


def get_subjects(request, classno):
    endpoint = "http://127.0.0.1:8000/api/classroom/subjects"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={"classno": classno}).json()
    if "status" in response:
        return []
    return response["subjects"]


def add_subject(request, classno, subjectName, image):
    endpoint = "http://127.0.0.1:8000/api/classroom/subjects/add"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={"classno": classno, 'subjectName': subjectName, 'image': image})
    return response


class subjectsView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def post(self, request, classno):
        form = addSubject(request.POST)
        if form.is_valid():
            classno = "class"+str(classno)
            print(form.cleaned_data['subjectName'], "-------------------")
            if add_subject(request, classno, form.cleaned_data['subjectName'], request.POST.get('imagefile')):
                print("subject added successfully :---------")
                return redirect('classroom_subjects', classno[5:])
        else:
            print("form is not valid ----------------------")
            classno = "class"+str(classno)
            subjects = get_subjects(request, classno)
            profile_data, aditional_data = get_Profiledata(request)
            context = {
                'profile': profile_data.json(),
                'otherdata': aditional_data,
                'subjects': subjects,
                'classroom': True,
                'form': form,
                'classno': classno
            }
            if request.user.is_staff:
                context['superUser':True]
            return render(request, 'subjects.html', context)

    def get(self, request, classno):
        form = addSubject(request.POST or None)
        print(classno, request, "-----------------------")
        classno = "class"+str(classno)
        subjects = get_subjects(request, classno)
        profile_data, aditional_data = get_Profiledata(request)
        context = {
            'profile': profile_data.json(),
            'otherdata': aditional_data,
            'subjects': subjects,
            'classroom': True,
            'form': form,
            'classno': classno
        }
        if request.user.is_staff:
            context['superUser':True]
        return render(request, 'subjects.html', context)


def get_lectures(request, classno, subject):
    endpoint = "http://127.0.0.1:8000/api/classroom/subjects/lectures"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={
        "classno": classno[5:],
        "subject": subject
    }).json()
    print("Data recieved ------------------------------------------")
    video_lectures_titles = response["LecturesTitle"]
    video_lectures_urls = response["LecturesLinks"]
    data = {}
    for titles, urls in zip(video_lectures_titles, video_lectures_urls):
        data[titles] = urls
    if len(data) == 0:
        return -1
    return data


def add_lectures(request, classno, subject, lectureTitle, lectureUrl):
    endpoint = "http://127.0.0.1:8000/api/classroom/subjects/lectures/add"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={'classno': classno[5:], 'subject': subject, 'lectureTitle': lectureTitle, 'lectureUrl': lectureUrl})


class LecturesView(LoginRequiredMixin, View):
    login_url = "/login"
    required_login_url = "redirect_to"

    def post(self, request, classno, subject):
        form = addLecture(request.POST)
        if form.is_valid():
            add_lectures(request, classno, subject,
                         form.cleaned_data['lecturesName'], form.cleaned_data['lectureUrl'])
        return self.get(request, classno, subject)

    def get(self, request, classno, subject):
        data = get_lectures(
            request, classno, subject)
        # form for adding new lectures
        form = addLecture()
        profile_data, aditional_data = get_Profiledata(request)
        context = {
            'profile': profile_data.json(),
            'otherdata': aditional_data,
            'form': form,
            'classroom': True,

            'classno': classno
        }
        if request.user.is_staff:
            context['superUser':True]
        if data != -1:
            context['videos_data'] = data
        else:
            context['nodata'] = True
            context['videos_data'] = {}
        return render(request, 'vidoeLectures.html', context)

# ----------------- end classroom -------------------


# friend section ----------------------------------------------
class FreindList(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        """Will show all the friends list available"""
        profile_data, aditional_data = get_Profiledata(request)
        friendlist_response = get_friend_list(request)

        context = {
            'profile': profile_data.json(),
            'otherdata': aditional_data,
            'following': True,
            'friendlist': friendlist_response.json(),
        }
        return render(request, 'friendlist.html', context)
# -------------------------------------------------------------


# ------------------- buy items ----------------------
def addItemfunction(request, dataToSent):
    endpoint = "http://127.0.0.1:8000/api/addstoreitem/"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data=dataToSent)


def getclasstype(st):
    if len(st) < 2:
        return '0' + str(st)
    else:
        return st


def getItemDetails(request, filter):
    endpoint = "http://127.0.0.1:8000/api/getBooksDetals/"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={'filter': filter})
    if filter == "Books":
        data = {}
        temp = {}

        for item in response.json():

            print(item['classtype'].split(" ")[1] > '09')
            if getclasstype(item['classtype'].split(" ")[1]) > '09':
                if item['classtype'] in temp:
                    temp[str(item['classtype'])].append(item)
                else:
                    temp[str(item['classtype'])] = [item]

            else:
                if item['classtype'] in data:
                    data[str(item['classtype'])].append(item)
                else:
                    data[str(item['classtype'])] = [item]

        for classtype in temp:
            data[classtype] = temp[classtype]
        return data
    elif filter == "Extra":
        data = {}
        for item in response.json():
            if item['classtype'] in data:
                data[str(item['classtype'])].append(item)
            else:
                data[str(item['classtype'])] = [item]
        return data


class BuyItem(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def post(self, request, item):
        form = addItemForm(request.POST)
        if form.is_valid():
            print('------------- form is valid ------------')
            data = {}
            data['title'] = form.cleaned_data['title']
            data['seller'] = form.cleaned_data['seller']
            data['price'] = form.cleaned_data['price']
            data['image'] = form.cleaned_data['image']
            data['noOfItems'] = form.cleaned_data['noOfItems']
            data['category'] = form.cleaned_data['category']
            data['classtype'] = form.cleaned_data['classtype']
            addItemfunction(request, data)
        else:
            return self.get(request, item, form)
        print(form.errors.as_data())
        print("--------------------")
        return self.get(request, item)

    def get(self, request, item, formm=None):
        profile_response, aditional_data = get_Profiledata(request)
        form = addItemForm(formm)
        context = {
            'profile': profile_response.json(),
            'otherdata': aditional_data,
            'form': form
        }

        if item == "Books":
            print("book buy")
            demo_data = getItemDetails(request, "Books")

        else:
            print("stationary buy")
            demo_data = getItemDetails(request, "Extra")
        context['bucket'] = demo_data
        context['classroom'] = True  # to hide the new post and filter button

        return render(request, 'buybooks.html', context)


def getSellerData(request, order_id):
    endpoint = "http://127.0.0.1:8000/api/getSellerData/"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={"order_id": order_id})
    return response.json()


def getItemDetail(request, id):
    endpoint = "http://127.0.0.1:8000/api/getItemDetal/"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={"order_id": id})
    return response.json()


class PlaceOrder(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def post(self, request, order_id):
        totalPriceToPay = request.POST['totalpriceHidden']
        if float(totalPriceToPay) == 0:
            return self.get(request, order_id)
        orderid = request.user.email+"_" + ''.join([chr(c) for c in numpy.random.randint(98, 112, 10)]) + "_" + \
            str(order_id)
        profile_response, aditional_data = get_Profiledata(request)

        itemDetail = getItemDetail(request, int(order_id))
        sellerInfo = getSellerData(request, int(order_id))
        payment_params = {}
        payment_params['body'] = dict(
            requestType="Payment",
            mid=paytm_id,
            websiteName="WEBSTAGING",
            orderId=orderid,
            callbackUrl=f"http://127.0.0.1:8000/check-payment/paytm/{encrypt(order_id)}/{encrypt(request.user.email)}/{encrypt(totalPriceToPay)}",
            txnAmount=dict(
                value=str(totalPriceToPay),
                currency="INR",
            ),
            userInfo=dict(
                custId=str(request.user.email)

            ),

        )
        checksum = PaytmChecksum.generateSignature(
            json.dumps(payment_params['body']), paytm_key)
        payment_params['head'] = dict(
            signature=checksum,
        )
        # for Staging
        url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={paytm_id}&orderId={orderid}"
        post_data = json.dumps(payment_params)
        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data=post_data, headers={
                                 "Content-type": "application/json"}).json()
        print(response)
        payment_page = dict(
            mid=paytm_id,
            txnToken=response['body']['txnToken'],
            orderId=orderid,

        )
        context = dict(
            profile=profile_response.json(),
            otherdata=aditional_data,
            data=payment_page
        )
        print("--------------------------------")
        print("payments parameters : ", payment_params)
        return render(request, 'callback.html', context)

    def get(self, request, order_id):
        profile_response, aditional_data = get_Profiledata(request)
        itemDetail = getItemDetail(request, int(order_id))
        sellerInfo = getSellerData(request, int(order_id))
        print("seller info", sellerInfo)
        context = {
            'profile': profile_response.json(),
            'otherdata': aditional_data,
            'product': itemDetail,
            'sellerInfo': sellerInfo

        }
        return render(request, 'placeorder.html', context)


def addOrdersInOrderLIst(id, email, totalprice, txnid):
    id = decrypt(id) or False
    email = decrypt(email) or False
    totalprice = int(float(decrypt(totalprice))) or False
    if id and email and totalprice:
        st = StoreItems.objects.get(id=id)
        ol = OrderedItmes.objects.create(items=st, datetime=str(datetime.now(
        )), totalPrice=totalprice, transectionId=txnid, buyer_email=email)

        try:
            ol.save()
        except:
            print("Ordered Not stored in database")
    else:
        print("parameters not satisfied for database orderedList")


@csrf_exempt
def paymentCheckingView(request, id, email, tprice):
    form = request.POST
    param_dict = dict(
        order_id=form.get('ORDERID'),
        payment_mode=form.get('PAYMENTMODE'),
        transection_id=form.get('TXNID'),
        bank_transection_id=form.get('BANKTXNID'),
        response_msg=form.get('RESPMSG'),
    )
    # profile_response, aditional_data = get_Profiledata(request)

    context = dict(
        # profile=profile_response.json(),
        # otherdata=aditional_data,
        status="Transection Failed",
    )
    param_data = {}
    if param_dict['response_msg'] != 'Txn Success':
        print("Transection failed")
    else:
        for key in form.keys():
            param_data[key] = form[key]

        checksum = request.POST.get('CHECKSUMHASH')
        isvaerified = PaytmChecksum.verifySignature(
            param_data, paytm_key, checksum)

        if isvaerified:
            print("Payment is verified")
            context['status'] = "Ordered Successfully"
            addOrdersInOrderLIst(
                id, email, tprice, param_dict['transection_id'])
            return render(request, 'transectionStatus.html', context)
        else:
            print("Payment is not verified")

            return render(request, 'transectionStatus.html', context)
    return render(request, 'transectionStatus.html', context)


class PaytmCallback(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request, id):
        print("product id :", id)
        return render(request, 'callback.html')
# -----------------------------------------------------


def getOrdersDetail(request):
    endpoint = "http://127.0.0.1:8000/api/getOrdersDetal/"
    response = requests.post(endpoint, headers={'Authorization': 'SecretToken '+str(
        request.session.get('token'))}, data={"email": request.user.email})
    return response.json()


class OrderView(LoginRequiredMixin, View):

    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        profile_response, aditional_data = get_Profiledata(request)
        getOrdersDetail(request)
        data = getOrdersDetail(request)
        for item in data:
            print(type(item))
            item['items'] = getItemDetail(request, item['items'])
            # item['items'] =

        context = {
            'profile': profile_response.json(),
            'otherdata': aditional_data,
            'orders': data
        }
        print("data : ", data)
        return render(request, 'orders.html', context)
