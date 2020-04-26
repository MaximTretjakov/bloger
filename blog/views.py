from django.http import HttpResponse
from django.views.generic import ListView, View, FormView
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage

from blog.models import Post
from blog.forms import EmailPostForm


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

