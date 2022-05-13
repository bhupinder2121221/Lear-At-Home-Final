
from django.contrib import admin
from .models import RegisterFormModel, Post, CustomUser, PostLikes, FollowdByModel, FolowersModel, viedo_lectures, subjects, Classes_and_subjects, Sellers, StoreItems, OrderedItmes
from django.utils.html import format_html


class RegisterAdminModel(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('fname', 'email', 'isauthor', 'profile', 'view')
    list_display_links = ('view', 'email')
    list_filter = ('dob', ('email', admin.EmptyFieldListFilter))

    def isauthor(self, obj):
        return format_html(f"<h5 style='color:red;'>{obj.fname}</h5>")

    def view(self, object):
        return format_html(
            f"<a href='{2}' style = 'width:80px;background-color:yellow;color:red;font-width:1rem;border:2px solid red;border-radius:20px;'>View</a>"
        )


# Register your models here.
admin.site.register(RegisterFormModel, RegisterAdminModel)
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(PostLikes)
admin.site.register(FollowdByModel)
admin.site.register(FolowersModel)
admin.site.register(viedo_lectures)
admin.site.register(subjects)
admin.site.register(Classes_and_subjects)
admin.site.register(OrderedItmes)
admin.site.register(StoreItems)
admin.site.register(Sellers)
