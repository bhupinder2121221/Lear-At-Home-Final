
from urllib import response
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import CustomUser, Post, PostLikes, RegisterFormModel, FolowersModel, FollowdByModel, Classes_and_subjects, Sellers, viedo_lectures, subjects, StoreItems, OrderedItmes
from api.mySerializer import PostSearlizers, UserSearilizer, ClassesandSubjects_Serializer, StoreItemsSerializer, SellerSerializer, GetOredersSearialoizer
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import generics, mixins, permissions, authentication
from datetime import datetime
from pytz import timezone
from .mypermissions import isValidUserPermission, freindListPermission
from .mytoken import myTokenAuthentication


@api_view(['GET'])
def detailed_Post(request):
    instance = Post.objects.all().first()
    print("instance ---------------", instance)
    data = PostSearlizers(instance).data
    print(data)
    return Response(data)


class Profiledata(APIView):
    authentication_classes = [myTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    permission_classes = [isValidUserPermission]

    def get_object(self, email):
        try:
            return CustomUser.objects.get(email=email)
        except:

            return None

    def get(self, request):
        user_id = request.data['username']
        instance = CustomUser.objects.filter(email=user_id)
        # print(instance)
        if len(instance):
            data = UserSearilizer(instance[0], many=False).data
            return Response(data)
        else:
            return Response({'status': 'User Not Found'}, status=404)

    def put(self, request):
        email = reguest.data['username']
        instance = self.get_object(email)
        if instance:
            slz = UserSearilizer(instance, data=request.data)
            if slz.is_valid():
                slz.save()
                return Response(slz.data)
            else:
                return Response(slz.errors)
        return Response({'status': 'Not Found'}, status=404)

    def delete(self, request):
        user_id = request.data['username']
        instance = self.get_object(user_id)
        if instance:
            instance.delete()
            instance.save()
            return Response({"status": "User deleted"}, status=200)
        else:
            return Response({'Status': 'User not found'}, status=404)


class friendListApi(APIView):
    authentication_class = [myTokenAuthentication]
    permission_classes = [freindListPermission]

    def post(self, request):

        username = request.data['username']
        jsondata = {}
        fl = FolowersModel.objects.get(email=username).followers.all()
        i = 0
        for n in fl:
            jsondata[n.email] = n.fname
            i += 1
        print(jsondata)
        return Response(jsondata)


class FollowersPostFilter(APIView):
    authentication_class = [myTokenAuthentication]

    def get(self, request):
        username = request.user.email
        fl = FolowersModel.objects.get(email=username).followers.all()
        print(fl)
        followersArray = []
        for n in fl:
            followersArray.append(n.email)
        print(followersArray)
        allposts = {'posts': []}

        pl = Post.objects.filter(author__in=followersArray).all()

        data = PostSearlizers(pl, many=True).data
        return Response(data)


class CreateProfile(generics.CreateAPIView):
    model = CustomUser
    serializer_class = UserSearilizer


class CreateUserSedicificPost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSearlizers

    def perform_create(self, slz):
        print("------------------------------------------------")
        pl = PostLikes.objects.create()
        pl.save()
        try:
            slz.save(postlike=pl)
            print("post made and saved successfully")
            return Response({'error': 'no error'})
        except:
            return Response({'error': 'Error in save'})


class DeleteUserSpecificPost(APIView):
    def post(self, request):
        username = request.user.email
        postid = int(request.data['post_id'])
        try:
            Post.objects.get(post_id=postid).delete()
        except:
            return Response({'status': '500'})
        return Response({'status': '200'})


class EditUserSpecificPost(APIView):
    def post(self, request):
        print("eneter in edit post api")
        username = request.user.email
        postid = int(request.data['post_id'])
        title = request.data['title']
        content = request.data['content']
        image = request.data.get('image', False)
        print("going for edditng db")
        try:
            p = Post.objects.get(post_id=postid)
            p.title = title
            p.content = content
            if image:
                p.image = image
            p.save()
            print("done")
            return Response({'status': '200'})
        except:
            print("error")
            return Response({'status': '500'})


class UserSpecificPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSearlizers
    lookup_field = 'post_id'


class FollowersView(APIView):
    authentication_classes = [myTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        # checking if it followed or not
        flTable = FolowersModel.objects.all().get(email=data['username'])
        fl = flTable.followers
        fl1 = fl.all()
        flobject = ""
        for follower in fl1:
            if follower.email == data['targetUserName']:
                flobject = follower
                break
        if flobject != "":
            fl.remove(flobject)
        else:
            fl.add(CustomUser.objects.get(email=data['targetUserName']))
        print("Follower Model ran successfully")

        followedMTable = FollowdByModel.objects.get(
            email=data['targetUserName'])
        followedM = followedMTable.follwedBy
        followedM1 = followedM.all()
        flobject = ""
        for f in followedM1:
            if f.email == data['username']:
                flobject = f
                break
        if flobject != "":
            followedM.remove(f)
        else:
            followedM.add(request.user)
        followedMTable.save()
        flTable.save()
        print("followed by Model ran success")

        return Response({'status': "Saved success"})


class GlobalPostsDetailView(APIView):
    def get(self, request, post_id=1):
        if request.user.is_authenticated:
            return redirect('userPostsDetalView', post_id=post_id)
        instance = Post.objects.get(post_id=post_id)
        if instance is None:
            return response({"Status": "Post Not Found"})
        data = PostSearlizers(instance).data
        return Response(data)

    def post(self, request):
        return Response({"Warning": "Cannot use POST command here in GlobalPostDetailView"})

    def delete(self, request):
        return Response({"Warning": "Cannot use DELETE command here in GlobalPostDetailView"})


class GlobalPostsListView(APIView):
    def get(self, request, post_id=None):
        instances = Post.objects.all().order_by("dateTime")
        data = PostSearlizers(instances, many=True).data
        return Response(data)

    def post(self, request):
        return Response({"Warning": "Cannot use POST command here in GlobalPostListView"})

    def delete(self, request):
        return Response({"Warning": "Cannot use DELETE command here in GlobalPostListView"})


# classroom----------------------
class GetClasses(APIView):
    def get(self, request):
        instances = Classes_and_subjects.objects.all().order_by('myclass')
        data = ClassesandSubjects_Serializer(instances, many=True).data
        return Response(data)

    def post(self, request):

        classno = request.data["classno"]
        classtype = request.data["classtype"]
        cl = Classes_and_subjects.objects.create(
            myclass="class"+str(classno),
            classtype=str(classtype))
        cl.save()
        return Response({'status': "database created"})


class GetSubjects(APIView):
    def post(self, request):
        classno = request.data["classno"]
        instance = Classes_and_subjects.objects.filter(
            myclass=classno)  # classno=class1
        if len(instance) == 0:
            return Response({"status": "not found"})
        else:
            subjects = {}
            for subject in instance[0].subject.all():
                subjects[subject.image] = subject.subject

            return Response({'subjects': subjects})


class AddSubjects(APIView):
    def post(self, request):
        classno = request.data["classno"]  # classno=class1
        subjectName = request.data["subjectName"]
        image = request.data["image"]
        sb = subjects.objects.create(subject=subjectName, image=image)
        sb.save()
        cl = Classes_and_subjects.objects.get(myclass=classno)
        cl.subject.add(sb)
        cl.save()
        return Response({"status": "database updated"})


class GetLectures(APIView):
    def post(self, request):
        classno = request.data["classno"]
        subjectName = request.data["subject"]
        cl = Classes_and_subjects.objects.get(myclass="class"+str(classno))
        sb = 0
        for subject in cl.subject.all():
            if subject.subject.lower() == subjectName.lower():
                sb = subject
                break
        video_lectures = []
        video_lectures_urls = []
        for video in sb.viedo_lectures.all():
            video_lectures.append(video.title)
            video_lectures_urls.append(video.video_url)
        data = {}
        data['LecturesTitle'] = video_lectures
        data['LecturesLinks'] = video_lectures_urls
        return Response(data)


class AddLectures(APIView):
    def post(self, request):
        classno = request.data["classno"]
        subjectName = request.data["subject"]
        lectureName = request.data["lectureTitle"]
        lectureUrl = request.data["lectureUrl"]
        cl = Classes_and_subjects.objects.get(myclass="class"+str(classno))
        sb = cl.subject.all()
        vlParent = 0
        vl = 0
        for subject in sb:
            if subject.subject.lower() == subjectName.lower():
                vlParent = subject
                vl = subject.viedo_lectures
                break
        vl_temp = viedo_lectures.objects.create(
            title=lectureName, video_url=lectureUrl)
        vl_temp.save()
        vl.add(vl_temp)
        vlParent.save()
        return Response({'status': 'Database changed'})


# buy items

class AddItem(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = StoreItemsSerializer


class GetItems(APIView):
    """Return items based on filter"""

    def post(self, request):
        filter_word = request.data['filter'].lower()
        si = StoreItems.objects.filter(
            category=filter_word).order_by('classtype').all()
        data = StoreItemsSerializer(si, many=True).data
        # print("data", data)
        return Response(data)


class GetSellerData(APIView):
    def post(self, request):
        order_id = request.data['order_id']
        sellername = StoreItems.objects.filter(id=order_id).all()

        sl = Sellers.objects.filter(
            name=sellername[0].seller.name).all().first()

        print(sl.name)
        data = SellerSerializer(sl).data
        # print(data)
        return Response(data)


class GetItemDetail(APIView):
    def post(self, request):
        orderid = request.data['order_id']
        # print(orderid)
        order = StoreItems.objects.filter(id=orderid).all()
        # print(order)
        if len(order) == 0:
            return Response({'status': "Order Not Found"})
        data = StoreItemsSerializer(order[0], many=False).data

        return Response(data)


class GetOrders(APIView):
    def post(self, request):
        useremail = request.data['email']
        o = OrderedItmes.objects.filter(buyer_email=useremail).all()
        data = GetOredersSearialoizer(o, many=True).data
        print(data)
        return Response(data)


class OrederItem(APIView):
    def post(self, request):
        data = request.data
        try:
            o = OrderedItmes.objects.create()
            o.save()
            return Response({'status': 'success'})
        except:
            return Response({'status': 'failed'})
