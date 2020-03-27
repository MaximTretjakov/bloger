from django.urls import path, re_path
from blog.views import PostDetail, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
            PostDetail.as_view(),
            name='post_detail'),
]
