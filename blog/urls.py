from django.urls import path, re_path
from blog.views import PostDetail, PostListView, PostShareView
from blog.views import PostDetail, PostListView, PostListPagination


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
            PostDetail.as_view(),
            name='post_detail'),
    re_path(r'^(?P<post_id>\d+)/share/$', PostShareView.as_view(), name='post_share'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', PostListPagination.as_view(), name='post_list_by_tag'),
    path('pagination/', PostListPagination.as_view(), name='post_list_pagination'),
]
