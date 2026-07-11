from rest_framework import permissions

class AdminOrReadOnly(permissions. IsAdminUser):
    
    
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" and admin_permission
    
    
# from rest_framework import permissions

# class AdminOrReadOnly(permissions.IsAdminUser):

#     def has_permission(self, request, view):

#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return bool(request.user and request.user.is_staff)