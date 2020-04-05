from django.http import HttpResponse
from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post


class PostDetail(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,
                                 slug=kwargs['post'],
                                 status='published',
                                 publish__year=kwargs['year'],
                                 publish__month=kwargs['month'],
                                 publish__day=kwargs['day'])

        return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostListPagination(View):
    def get(self, request, *args, **kwargs):
        object_list = Post.published.all()
        paginator = Paginator(object_list, 3)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
