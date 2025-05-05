import logging
from typing import Literal

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from posts.models import Posts, Images, Categories
#импорт классов django и модели постов, изображений и категорий 

logger = logging.getLogger()
#создание логгера

class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        #обработка GET запроса
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        #получаем все посты
        return render(
            request=request, template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active
            }
        )
        #возвращаем страницу с постами и передаем информацию о пользователе


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        #обработка GET запроса
        is_active = request.user.is_active
        categories = Categories.objects.all()
        #получаем все категории
        if not categories:
            return HttpResponse(
                content="<h1>Something went wrong</h1>"
            )
        #проверяем есть ли категории
        if not is_active:
            return redirect(to="login")
        #если пользователь не авторизован перенаправляем на страницу логина
        return render(
            request=request, template_name="post_form.html",
            context={"categories": categories}
        )
        #возвращаем страницу с формой поста и передаем категории

    def post(self, request: HttpRequest) -> HttpResponse:
        #обработка POST запроса
        images = request.FILES.getlist("images")
        #получаем список изображений из формы
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        #создаем пост
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) for img in images]
        Images.objects.bulk_create(imgs)
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        return redirect(to="base")


class ShowDeletePostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse: 
        #обработка GET запроса
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            post = None
        author = False
        #проверяем есть ли пост
        if request.user == post.user:
            author = True
        #проверяем является ли пользователь автором поста
        return render(
            request=request, template_name="pk_post.html",
            context={
                "post": post,
                "author": author
            }
        )
        #возвращаем страницу с постом и передаем информацию о посте и авторе

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        #обработка POST запроса
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            pass
        #проверяем есть ли пост
        if request.user != post.user:
            return HttpResponse(
                "<h1>У тебя здесь нет власти</h1>"
            )
        #если пользователь не автор поста выводим сообщение
        post.delete()
        return redirect(to="base")
        #удаляем пост и перенаправляем на главную страницу


class LikesView(View):
    def post(
        #обработка POST запроса
        self, request: HttpRequest, 
        pk: int, action: Literal["like", "dislike"]
        #pk - id поста, action - действие (лайк или дизлайк)
    ):
        client = request.user #получаем пользователя
        if not client.is_active:
            return
        #если пользователь не авторизован, ничего не делаем
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return
        #проверяем есть ли пост
        result = {}
        if action == "like":
            post.likes += 1
            result["likes"] = post.likes
        elif action == "dislike":
            post.dislikes += 1
            result["dislikes"] = post.dislikes
        #если действие лайк или дизлайк, увеличиваем счетчик
        post.save(update_fields=["likes", "dislikes"])
        #сохраняем пост
        return JsonResponse(data=result)
        #возвращаем json ответ с количеством лайков и дизлайков
