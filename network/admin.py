from django.contrib import admin
from .models import Post, FriendRequest

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'posted_at')
    search_fields = ('author__username', 'content')
    ordering = ('-posted_at',)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'accepted', 'timestamp')
    list_filter = ('accepted',)
    search_fields = ('sender__username', 'receiver__username')
    ordering = ('-timestamp',)