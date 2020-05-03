from django.http import HttpResponse
from django.views.generic import ListView, View, FormView
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taggit.models import Tag

from blog.models import Post, Comment
from blog.forms import EmailPostForm, CommentForm


class PostDetail(FormView):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,
                                 slug=kwargs['post'],
                                 status='published',
                                 publish__year=kwargs['year'],
                                 publish__month=kwargs['month'],
                                 publish__day=kwargs['day'])

        comments = post.comments.filter(active=True)

        comment_form = CommentForm()
        return render(request, 'blog/post/detail.html', {'post': post,
                                                         'comments': comments,
                                                         'comment_form': comment_form})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post,
                                 slug=kwargs['post'],
                                 status='published',
                                 publish__year=kwargs['year'],
                                 publish__month=kwargs['month'],
                                 publish__day=kwargs['day'])

        comments = post.comments.filter(active=True)

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return render(request, 'blog/post/detail.html', {'post': post,
                                                         'comments': comments,
                                                         'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostShareView(FormView):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'], status='published')
        form = EmailPostForm()
        sent = False
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'], status='published')

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            msg = EmailMessage(subject, message, to=['000.maximtretyakov.000@gmail.com'])
            msg.send(fail_silently=False)

        sent = True
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class PostListPagination(View):
    def get(self, request, *args, **kwargs):
        object_list = Post.published.all()

        tag = None
        if kwargs['tag_slug']:
            tag = get_object_or_404(Tag, slug=kwargs['tag_slug'])
            object_list = object_list.filter(tags__in=[tag])

        paginator = Paginator(object_list, 3)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

