from django.shortcuts import render, redirect
from .models import User, ConfirmString
from . import forms
import hashlib, datetime
from django.conf import settings
# Create your views here.
def hash_code(s, salt="mysite"):
    h = hashlib.sha256()
    s += salt

    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/user/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        return redirect('/user/index/')
    context = {}
    return render(request, 'login/index.html', context)

def login(request):
    if request.session.get('is_login', None):
        return redirect("/user/index")

    if request.method == "POST":
        loginForm = forms.UserForm(request.POST)
        message = 'please check the data'
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']

            try:
                user = User.objects.get(name=username)

                if not user.has_confirmed:
                    message = "This User doesn't Confirm！"
                    return render(request, 'login/login.html', locals())

                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    return redirect('/user/index')
                else:
                    message = "password is incorrect"
            except:
                message = "user doesn't exists"
            return render(request, 'login/login.html', locals())
    loginForm = forms.UserForm()
    return render(request, 'login/login.html', locals())
    # if request.method == "POST":
    #     username = request.POST.get('username', None)
    #     password = request.POST.get('password', None)
    #     message ="all input must be here"
    #
    #     if username and password:
    #         username = username.strip()
    #
    #         try:
    #             user = User.objects.get(name=username)
    #
    #             if user.password == password:
    #                 print(username, password)
    #                 return redirect('/user/index/')
    #             else:
    #                 message="password is incorrect"
    #         except:
    #
    #             message = "user doesn't exists"
    #             return render(request, "login/login.html", {'message':message, })
    #         if user.password == password:
    #
    #             print(username, password)
    #             return redirect('/user/index/')
    # context = {}
    # return render(request, 'login/login.html', context)

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/user/index/")

    if request.method == "POST":
        registerForm = forms.RegisterForm(request.POST)
        message = 'please check the data'
        if registerForm.is_valid():
            username = registerForm.cleaned_data['username']
            password_first = registerForm.cleaned_data['password_first']
            password_second = registerForm.cleaned_data['password_second']
            email = registerForm.cleaned_data['email']
            sex = registerForm.cleaned_data['sex']

            if password_first != password_second:  # 判断两次密码是否相同
                message = "two password is different！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = 'The User exists'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = 'The email exists'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password_first)
                new_user.email = email
                new_user.sex = sex
                new_user.save()


                code = make_confirm_string(new_user)
                send_email(email, code)
                message = "Please Confirm email"

                return render(request, 'login/confirm.html', locals())

    registerForm = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/user/index/")
    request.session.flush()
    context = {}
    return redirect("/user/index/")

def confirm(request):
    code = request.GET.get('code', None)
    message = 'Need you confirm'
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = "Invalid request"
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time.replace(tzinfo=None)
    now = datetime.datetime.now()
    #replace timezone
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = 'Your Email is timeout, please Re-Register'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = 'Thanks Your Confirm'
        return render(request, 'login/confirm.html', locals())