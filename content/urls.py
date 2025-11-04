# content/urls.py

from django.urls import path
from .views import (
    PostListCreateView, 
    PostDetailView, 
    NewsFeedView, 
    CommentListCreateView, 
    CommentDeleteView,
    LikeView
)

urlpatterns = [
    # Posts
    # GET /api/posts/ (List all posts) & POST /api/posts/ (Create new post)
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    
    # GET/PUT/DELETE /api/posts/{post_id}/
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # News Feed
    # GET /api/feed/ (View posts from followed users)
    path('feed/', NewsFeedView.as_view(), name='news-feed'), 
    
    # Comments
    # GET /api/posts/{post_id}/comments/ (List comments) 
    # POST /api/posts/{post_id}/comments/ (Create comment)
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    
    # DELETE /api/comments/{comment_id}/
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

    path('posts/<int:post_id>/like/', LikeView.as_view(), name='like-unlike'),
]