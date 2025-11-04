# users/views.py

from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer # <-- Import ProfileSerializer
from .models import Profile # <-- Import Profile model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfProfile
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from .models import Follow, Profile
from rest_framework.response import Response

# User Register View (Existing)
class UserRegisterView(generics.CreateAPIView):
    # ... (Keep existing code)
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# Profile Detail and Update View (NEW)
class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id' # Tells DRF to look up the profile by the user's ID
    permission_classes = [IsAuthenticated, IsOwnerOfProfile]
    
    # Permission: Only authenticated users can access this, and only the owner can update
    def get_permissions(self):
        # Allow any authenticated user to GET (view) a profile
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        # Only the owner can PUT (update) the profile
        return [IsAuthenticated(), IsOwnerOfProfile()] # type: ignore

    # We need a custom permission to check if the user updating the profile is the owner
    # For now, let's keep it simple and enforce IsAuthenticated for all
    # We will refine permissions in a moment if you want to test the update functionality.
    
    # Simpler permission setup for testing: Anyone logged in can view, only logged in can update
    # Note: We must explicitly restrict updates to the owner for security!
    permission_classes = [IsAuthenticated]
    
    # Custom check for update permission (Required for security)
    def perform_update(self, serializer):
        profile = self.get_object()
        # Only allow the user to update their own profile
        if self.request.user != profile.user:
            raise permissions.PermissionDenied("You do not have permission to update this profile.")
        serializer.save()


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # The user being followed (the target user)
        try:
            followed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND) # type: ignore

        follower_user = request.user # The logged-in user (the source user)

        # 1. Prevent Self-Following
        if follower_user == followed_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST) # type: ignore

        # 2. Check if already following
        if Follow.objects.filter(follower=follower_user, followed=followed_user).exists():
            return Response({"detail": "Already following this user."}, status=status.HTTP_409_CONFLICT) # type: ignore

        # 3. Create the Follow relationship
        Follow.objects.create(follower=follower_user, followed=followed_user)
        return Response({"detail": f"Successfully followed {followed_user.username}."}, status=status.HTTP_201_CREATED) # type: ignore

    def delete(self, request, user_id):
        # The user being unfollowed
        try:
            followed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND) # type: ignore

        follower_user = request.user

        # 1. Attempt to find and delete the relationship
        follow_instance = Follow.objects.filter(follower=follower_user, followed=followed_user)
        
        if not follow_instance.exists():
            return Response({"detail": "You are not currently following this user."}, status=status.HTTP_404_NOT_FOUND) # type: ignore

        follow_instance.delete()
        return Response({"detail": f"Successfully unfollowed {followed_user.username}."}, status=status.HTTP_204_NO_CONTENT) # type: ignore