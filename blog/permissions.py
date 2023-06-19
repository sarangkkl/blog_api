from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # print("has_object_permission")
        if request.method == 'GET':
            return True  # Allow unrestricted access for GET requests
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print("has_object_permission")
        if request.method == 'GET':
            return True  # Allow unrestricted access for GET requests
        return obj.author == request.user
