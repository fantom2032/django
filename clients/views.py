import logging

from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from clients.models import Client
#импорт классов django и модель клиента

logger = logging.getLogger()
#создание логгера

class RegistrationView(View):
    """Registration controller. 
    There will be only get & post methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        #обработка GET запроса
        return render(request=request, template_name="reg.html")#возвращает страницу регистрации
    
    def post(self, request: HttpRequest) -> HttpResponse:
        #обработка POST запроса
        #получаем данные из формы
        username = request.POST.get("username")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")
        if len(raw_password) < 8: #проверяем длину пароля
            messages.error(
                request=request, message="Password is too short" #если пароль меньше 8 символов выводим сообщение
            )
            return render(request=request, template_name="reg.html")#возвращает страницу регистрации
        try:
            Client.objects.create(
                email=email, username=username,
                password=make_password(raw_password)
            )
            #создаем объект клиента и хешируем пароль
            messages.info(
                request=request, message="Success Registration"
            )
            #выводим сообщение об успешной регистрации
            return render(
                request=request, template_name="reg.html"#возвращает страницу регистрации
            )
            
        
        except IntegrityError as ie:
            logger.error(msg="Ошибка уникальности поля", exc_info=ie)
            messages.error(
                request=request, message="Wrong login or email"
            )
            return render(request=request, template_name="reg.html")
            #если есть ошибка уникальности поля, выводим сообщение
        except Exception as e:
            logger.error(msg="Something happened", exc_info=e)
            messages.error(request=request, message=str(e))
            return render(request=request, template_name="reg.html")
            #если произошла другая ошибка, выводим сообщение


class LoginView(View):
    """Login Controller."""

    def get(self, request: HttpRequest) -> HttpResponse:
        #обработка GET запроса
        return render(request=request, template_name="login.html")
        #возвращает страницу авторизации
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        #получаем данные из формы
        client: Client | None = authenticate(
            request=request, 
            username=username, 
            password=password,
        )
        #проверяем данные
        if not client:
            messages.error(
                request=request, 
                message="Wrong username or password"
            )
            #если данные не валидны выводим сообщение
            return render(request=request, template_name="login.html")
            #возвращает страницу логина
        login(request=request, user=client)
        return redirect(to="base")
        #если данные правильные, регистрируем пользователя и перенаправляем на главную страницу


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        #обработка GET запроса
        is_active = request.user.is_active
        #проверяем активность пользователя
        if not is_active:
            return HttpResponse("Вы не авторизованы")
        #если пользователь не активен выводим сообщение
        logout(request=request)
        #выходим из системы
        return redirect(to="base")
        #перенаправляем на главную страницу
    
