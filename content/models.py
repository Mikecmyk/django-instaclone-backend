# content/models.py

from django.db import models
from django.contrib.auth.models import User

# Post Model
class Post(models.Model):
    # Foreign Key: A post belongs to one user. CASCADE means if the user is deleted, the post is too.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # Content Fields
    text_content = models.TextField(blank=True, null=True)
    
    # Note: We'll set up MEDIA_ROOT later for these file fields
    image_file = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video_file = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Post discovery fields
    # We will handle hashtag extraction/tagging later, but storing the original text is key
    
    class Meta:
        ordering = ['-created_at'] # Default ordering: newest posts first

    def __str__(self):
        # Display the first 50 characters of the post content
        return f"Post by {self.user.username}: {self.text_content[:50]}..."
    

class Comment(models.Model):
    # The user who posted the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The post the comment belongs to
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # The content of the comment
    text_content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
    

class Like(models.Model):
    # The user who liked the post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The post that was liked
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a post once
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on Post {self.post.id}"