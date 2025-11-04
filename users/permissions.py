# users/permissions.py

from rest_framework import permissions

class IsOwnerOfProfile(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    Assumes the view uses 'user_id' for lookup and the object has a 'user' field.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (e.g., GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile (e.g., PUT/PATCH)
        return obj.user == request.user