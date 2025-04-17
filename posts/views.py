import logging

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from posts.models import Posts, Images, Comments


logger = logging.getLogger()


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        posts: QuerySet[Posts] = Posts.objects.all()
        if not posts:
            return render(
                request=request, template_name="posts.html",
                status=404,
            )
        return render(
            request=request, template_name="posts.html", 
            context={"posts": posts}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass

class CommentsView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def like(self, request, *args, **kwargs):
        pass