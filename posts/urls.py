from django.urls import path

from posts.views import PostsView
from .views import CommentsView

urlpatterns = [
    path(route="", view=PostsView.as_view(), name="posts"),
    path('comments/', CommentsView.as_view(), name='comments'),
]
