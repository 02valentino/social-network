from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'network/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
