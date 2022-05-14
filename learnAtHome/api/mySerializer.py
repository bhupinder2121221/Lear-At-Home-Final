
from dataclasses import field
from rest_framework import serializers
from blog.models import Post, CustomUser, Classes_and_subjects, StoreItems, Sellers, OrderedItmes


class ClassesandSubjects_Serializer(serializers.ModelSerializer):
    """This is to get and post all the available classes for student"""
    class Meta:
        model = Classes_and_subjects
        fields = "__all__"


class StoreItemsSerializer(serializers.ModelSerializer):
    """This serializer is for storing the buying items for store"""
    class Meta:
        model = StoreItems
        fields = '__all__'


class GetOredersSearialoizer(serializers.ModelSerializer):
    """This will give detail of all orders"""
    class Meta:
        model = OrderedItmes
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    """ This will give info of seller in dict"""
    class Meta:
        model = Sellers
        fields = '__all__'


# class SellerSerializer(serializers.ModelSerializer):
#     """ This will give info of seller in dict"""
#     class Meta:
#         model: Sellers
#         fields = '__all__'


class UserSearilizer(serializers.ModelSerializer):
    """ This serializer will convert the model to json format """
    class Meta:
        model = CustomUser
        fields = [
            'fname',
            'lname',
            'email',
            'dob',
            'is_staff',
            'is_superuser',
            'profile',
        ]


class PostSearlizers(serializers.ModelSerializer):
    """ This searlizer will only convert model to its equivalent json data"""
    class Meta:
        model = Post
        fields = [
            'post_id',
            'title',
            'content',
            'author',
            'dateTime',
            'image'
        ]
