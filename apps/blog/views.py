from django.views.generic import DetailView, ListView

from apps.blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 12
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("category")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
