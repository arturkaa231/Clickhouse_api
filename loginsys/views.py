from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def  login(request):
    args={}
    #Заносим в словарь уникальный код
    args.update(csrf(request))
    #Если метод запроса POST, получаем из формы данные, заполненные пользователем и авторизируем пользователя
    if request.POST:
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
    #Если пользователь существует и данные введены правельно, тогда создается сессия для пользователя
        if user is not None:
            auth.login(request,user)
            return redirect('login.html',args)
    # Если пользователь на найден, добавляем в словарь login error
        else:
            args['login_error']="User is not found"
            return render_to_response('login.html',args)
    # Если пользователь просто нажал войти, отобразится форма для ввода имени и пароля
    else:
        return render_to_response('login.html',args)
# Деавторизация
def logout(request):
    auth.logout(request)
    return redirect('/')
#Регистрация пользователя
def register(request):
    args={}
    args.update(csrf(request))
    args['form']=UserCreationForm()
    if request.POST:
        new_user_form=UserCreationForm(request.POST)
        if new_user_form.is_valid:
            new_user_form.save()
            newuser=auth.authenticate(username=new_user_form.cleaned_data['username'], password=new_user_form.cleaned_data['password2'])
            auth.login(request,newuser)
            return redirect('/')
        else:
            args['form']=new_user_form
    return render_to_response('register.html',args)