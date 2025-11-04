# users/urls.py

from django.urls import path
from .views import UserRegisterView, ProfileDetailUpdateView
from .views import UserRegisterView, ProfileDetailUpdateView, FollowView

urlpatterns = [
    # Auth
    path('register/', UserRegisterView.as_view(), name='register'),
    
    # Profile Endpoints
    path('profiles/<int:user_id>/', ProfileDetailUpdateView.as_view(), name='profile-detail-update'),

    path('users/<int:user_id>/follow/', FollowView.as_view(), name='follow-unfollow'),
]