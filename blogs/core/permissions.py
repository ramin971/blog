from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(
                (str(request.user.id) == view.kwargs.get('pk')) and
                request.user.is_authenticated
                
            )