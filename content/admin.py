# content/admin.py

from django.contrib import admin
from .models import Post, Comment, Like # Ensure you import all models

# Use a custom ModelAdmin class to control the display
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text_content', 'image_file', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text_content', 'user__username')
    # Fields that should appear on the detail page (including the file fields)
    fields = ('user', 'text_content', 'image_file', 'video_file', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

# Register your models using the custom admin class
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)