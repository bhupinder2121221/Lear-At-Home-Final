
from django.contrib import admin
from django.urls import path, include
from blog.views import Login_Page, homePage, DeletePostView, register_page, logout_page, New_PostPage, postlikeView, followedView, friendPostView, ClassroomHome, BuyItem, subjectsView, LecturesView, FreindList, PlaceOrder, PaytmCallback, paymentCheckingView, OrderView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls, name='adminUrl'),



    #     paytm--------------------
    path('paytm/callback/', PaytmCallback.as_view(), name="paytm-callback"),
    path('place-order/<str:order_id>/',
         PlaceOrder.as_view(), name="placeorederView"),
    path('check-payment/paytm/<str:id>/<str:email>/<str:tprice>',
         paymentCheckingView, name='checktransection'),
    # --------------------------------------------------------
    # ------------orders ----------------
    path('orders/', OrderView.as_view(), name="orderview"),
    # ------------------------------------

    path('classroom/', ClassroomHome.as_view(), name="classroosmHome"),
    path('classroom/<str:classno>/subjects/',
         subjectsView.as_view(), name="classroom_subjects"),
    path('friend-list/', FreindList.as_view(), name="friendlistView"),
    path('classroom/<str:classno>/subjects/<str:subject>',
         LecturesView.as_view(), name="video_lecturesPage"),
    path('buy/<str:item>', BuyItem.as_view(), name="buyitem"),
    path('login/', Login_Page.as_view(), name='loginUrl'),
    path('', homePage, name='defaultHomeUrl'),
    path('filter-<str:filter>/', homePage, name='defaultHomeUrl'),
    path('page-<int:pageno>/', homePage, name='homeUrl'),
    path('page-<int:pageno>/filter-<str:filter>/', homePage, name='homeUrl'),
    path('page-<int:pageno>/friendPost-<str:friendEmail>/',
         friendPostView.as_view(), name="friendsPostsURL"),
    path('page-<int:pageno>/friendPost-<str:friendEmail>/pgno-<int:pgnumber>/',
         friendPostView.as_view(), name="friendsPostsURL"),
    path('page-<int:pageno>/friendPost-<str:friendEmail>/filter-<str:filter>/',
         friendPostView.as_view(), name="friendsPostsURL"),
    path('page-<int:pageno>/friendPost-<str:friendEmail>/pgno-<int:pgnumber>/filter-<filter>/',
         friendPostView.as_view(), name="friendsPostsURL"),
    path('page-<int:pageno>/pagelike-<int:post_id>/redirecturl-<str:redirecturl>',
         postlikeView, name="postlikeview"),
    path('page-<int:pageno>/pagefollowed-<str:SecondEmail>/redirecturl-<str:redirecturl>',
         followedView, name="followedURL"),
    path('register/', register_page, name='registerUrl'),
    path('deletepost/<str:postid>/',
         DeletePostView.as_view(), name="deletePost"),
    path('logout', logout_page, name='logoutUrl'),
    path('makepost', New_PostPage.as_view(), name="newPostUrl"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
