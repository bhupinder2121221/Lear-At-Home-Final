from rest_framework import permissions
class freindListPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.user.is_authenticated:
            return True
        return False

class isValidUserPermission(permissions.BasePermission):

    def has_permission(self,request,view):
        # print(request.user.get_all_permissions())
        if request.user.is_authenticated:
            print("The user is authenticated")
            print(request.user)
            return True
        print("The user is not authenticated")
        print(request.user)
        return False

    def has_object_permission(self,request,view,object):
        #here object is object of profile model that we want to access
        print("has_object_permissions")
        print(object.email)
        print(request.user.email)
        if object.email == request.user.email:
            print("here the user is assccessingits own profile")
            return True
        print("You cannot access anyones profile")
        return False