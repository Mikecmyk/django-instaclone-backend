# content/serializers.py

from rest_framework import serializers
from .models import Post
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # Read-only field to show the username of the post creator
    username = serializers.CharField(source='user.username', read_only=True)
    image_file = serializers.ImageField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    # MOVE THIS METHOD INSIDE THE CLASS
    def get_likes_count(self, obj):
        # obj is the Post instance. We access the 'likes' related manager and count them.
        return obj.likes.count()
    
    class Meta:
        model = Post
        fields = (
            'id', 'user', 'username', 'text_content', 
            'image_file', 'video_file', 'created_at', 'updated_at',
            'likes_count',
        )
        # 'user' field will be set automatically on creation
        read_only_fields = ('user', 'id', 'created_at', 'updated_at')
        
class CommentSerializer(serializers.ModelSerializer):
    # Read-only field to show the username of the comment creator
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'post', 'text_content', 'created_at')
        read_only_fields = ('user', 'post', 'id', 'created_at')