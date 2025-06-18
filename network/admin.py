from django.contrib import admin
from .models import Post, Follow

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'timestamp')
    search_fields = ('author__username', 'content')
    ordering = ('-created_at',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created')
    search_fields = ('follower__username', 'following__username')