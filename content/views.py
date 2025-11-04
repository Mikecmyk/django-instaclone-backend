# content/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from users.permissions import IsOwnerOfProfile # We will reuse IsOwnerOfProfile logic slightly
from users.models import Follow
from .models import Like

# Note: We need a custom permission for Posts. Let's create it quickly.

class IsPostOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a post to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (POST, PUT, DELETE) are only allowed to the owner of the post.
        return obj.user == request.user


# 1. View for GET /api/posts/ and POST /api/posts/
class PostListCreateView(generics.ListCreateAPIView):
    # Retrieve a list of all posts (or just posts from people the user follows, later)
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Automatically set the 'user' field to the logged-in user upon creation
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        # We explicitly return the default context and ensure 'request' is present.
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# 2. View for GET/PUT/DELETE /api/posts/{post_id}/
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Permission: Anyone authenticated can view (GET), but only the owner can update/delete
    permission_classes = [permissions.IsAuthenticated, IsPostOwner]
    lookup_field = 'pk' # The default lookup field for DRF is 'pk' (primary key/id)

    def get_serializer_context(self):
        # This tells the serializer (PostSerializer) what the current request is, 
        # allowing it to construct absolute URLs for file fields.
        return {'request': self.request}


class NewsFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 1. Get the current logged-in user
        user = self.request.user
        
        # 2. Get the IDs of all users the current user is FOLLOWING
        # user.following is the related_name we set on the Follow model
        # .values_list('followed_id', flat=True) efficiently returns a list of IDs
        following_ids = Follow.objects.filter(follower=user).values_list('followed_id', flat=True)

        # 3. Filter Posts: Show posts only from the users in the 'following_ids' list.
        #    We also include the user's own posts to populate the feed initially
        #    (Many social apps include the user's own content in their primary feed).
        queryset = Post.objects.filter(
            user_id__in=following_ids  # Posts from people they follow
        ).order_by('-created_at')

        return queryset
    

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer # type: ignore
    permission_classes = [permissions.IsAuthenticated]

    # This ensures we only return comments for the post specified in the URL
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('created_at') # type: ignore

    # This ensures we link the comment to the logged-in user AND the post from the URL
    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
        except Post.DoesNotExist:
            raise serializers.ValidationError({"detail": "Post not found."}) # type: ignore
            
        serializer.save(user=self.request.user, post=post)


# 2. View for DELETE /api/comments/{pk}/
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all() # type: ignore
    serializer_class = CommentSerializer # type: ignore
    # Custom permission to ensure only the owner can delete the comment
    permission_classes = [permissions.IsAuthenticated, IsPostOwner] # We will use IsPostOwner's logic, but tailored for a comment object. Let's create a specific IsCommentOwner.

# Since IsPostOwner checks obj.user, we need a slight adjustment for comments. 
# Let's adjust the permissions temporarily until we refactor:
# For now, let's use IsPostOwner as a placeholder and ensure the object being checked is the comment.
# Note: IsPostOwner works for any object with a 'user' foreign key field.

# Let's ensure our IsPostOwner class works:
# It checks: return obj.user == request.user
# Since Comment has a 'user' field, this permission works for comments too! 
# We'll use: permission_classes = [permissions.IsAuthenticated, IsPostOwner]


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        # The post being liked
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # 1. Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_409_CONFLICT)

        # 2. Create the Like
        Like.objects.create(user=user, post=post)
        return Response({"detail": "Post successfully liked."}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        # The post being unliked
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # 1. Attempt to find and delete the relationship
        like_instance = Like.objects.filter(user=user, post=post)
        
        if not like_instance.exists():
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_404_NOT_FOUND)

        like_instance.delete()
        return Response({"detail": "Post successfully unliked."}, status=status.HTTP_204_NO_CONTENT)