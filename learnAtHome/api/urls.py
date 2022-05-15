
from django.urls import path, re_path
from .views import detailed_Post, GlobalPostsListView, GlobalPostsDetailView, UserSpecificPostDetailView, CreateUserSedicificPost, Profiledata, CreateProfile, FollowersView, friendListApi, FollowersPostFilter, DeleteUserSpecificPost, GetClasses, GetSubjects, AddSubjects, GetLectures, AddLectures, AddItem, GetItems, GetItemDetail, GetSellerData, GetOrders
from rest_framework.authtoken.views import obtain_auth_token

# jwt token authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [

    path('', GlobalPostsListView.as_view(), name="allPost"),

    # for token authentication --------------------------------
    path('gettoken/', obtain_auth_token),
    path('getJwtToken/', TokenObtainPairView.as_view(), name='getjwttoken'),
    path('refreshJwtToken/', TokenRefreshView.as_view(), name='refreshjwttoken'),
    path('verifyJwtToken/', TokenVerifyView.as_view(), name='veifyjwttoken'),
    # ------------------------------------------------------------


    #  Buy Items -------------------------------------------
    path('addstoreitem/', AddItem.as_view(), name="addstoreitem"),
    path('getBooksDetals/', GetItems.as_view(), name="getBooksDetals"),
    path('getItemDetal/', GetItemDetail.as_view(), name="getItemDetalApi"),
    path('getSellerData/', GetSellerData.as_view(), name="getSellerDataAPI"),
    path('getOrdersDetal/', GetOrders.as_view(), name='getOrdersdatil'),
    # -------------------------------------------------------


    # classroom ----------------------------------------------------
    path('classroom/', GetClasses.as_view(), name="get_all_classes"),
    path('classroom/subjects', GetSubjects.as_view(),
         name="get_subjects_of_classno"),
    path('classroom/subjects/add', AddSubjects.as_view(),
         name="add_subject_in_class"),
    path('classroom/subjects/lectures', GetLectures.as_view(),
         name="Get_lectures_of_subject"),
    path('classroom/subjects/lectures/add',
         AddLectures.as_view(), name="add_lecture_in_subject"),
    # ------------------------------------------------------------

    #   posts ------------------------------------------------------
    path('deletepost/', DeleteUserSpecificPost.as_view(), name="deletePost"),
    path('filterFollowers/', FollowersPostFilter.as_view(), name="filterfollowing"),
    path('createProfile/', CreateProfile.as_view()),
    path('profile/', Profiledata.as_view(), name="profile"),
    path("friendlist/", friendListApi.as_view(), name="friendListApi"),
    re_path(r'^(?:post-(?P<post_id>[0-9]{1,}))/$',
            GlobalPostsDetailView.as_view(), name="detailPost"),
    path('user/', CreateUserSedicificPost.as_view(), name="createuserPost"),
    path('user/follower/', FollowersView.as_view(), name='followURLAPI'),
    re_path(r'^user/(?:post-(?P<post_id>[0-9]{1,}))/$',
            UserSpecificPostDetailView.as_view(), name="userPostsDetalView")
]
