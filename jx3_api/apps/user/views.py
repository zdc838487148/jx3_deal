import json
import re
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from . import user_forms, models
from django.http import JsonResponse
from article import models as article_models
from jx3_api.libs.sms import sendmsg
from django.core.cache import cache
from jx3_api.libs import sms
from django.contrib import auth
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from utils.article_pages import Pagination
from django.db.models import F
from player import models as playermodels


# 测试
def test(request):
    print(request.user)
    return HttpResponse("ok")


# 账号注册
class Resister(View):

    def get(self, request):
        print("run register get")
        form_obj = user_forms.Register()

        return render(request, 'register.html', locals())

    def post(self, request):
        print("run register post")
        back_dic = {
            "status_code": 1,
            "msg": "注册成功",
        }

        form_obj = user_forms.Register(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            data.pop("re_password")
            file_obj = request.FILES.get("avatar_file")
            if file_obj:
                data["avatar"] = file_obj
            models.UserInfo.objects.create_user(**data)
            jx3_name = data.get("jx3_name")
            user_obj = models.UserInfo.objects.filter(jx3_name=jx3_name).first()
            article_models.Blog.objects.create(site_name=user_obj.jx3_name,userinfo=user_obj)

            back_dic["url"] = reverse("home")
            return JsonResponse(back_dic)
        else:
            print(11)
            back_dic["status_code"] = 0
            back_dic["msg"] = form_obj.errors
            print(form_obj.errors)
            return JsonResponse(back_dic)


# 发送短信
class Sms(View):
    def post(self, request):
        print(18888888)
        phone = request.POST.get("phone")
        print("后端拿到的phone：", phone)
        sms.sendmsg(phone)
        return JsonResponse({"ok": "ok"})


# 短信注册
class RegisterPhone(View):
    back_dic = {
        "status_code": 1,
        "msg": "注册成功",
    }

    def get(self, request):
        form_obj = user_forms.RegisterPhone()

        return render(request, "register_phone.html", locals())

    def post(self, request):
        back_dic = {
            "status_code": 1,
            "msg": "注册成功",
        }
        # back_dic = self.back_dic
        # back_dic["msg"] = "zdc"
        # print(back_dic, self.back_dic)
        form_obj = user_forms.RegisterPhone(request.POST)
        if form_obj.is_valid():
            web_code = request.POST.get("web_code")
            if not web_code:
                back_dic["status_code"] = 0
                form_obj.errors["code"] = ["验证码不能为空", ]
                back_dic["msg"] = form_obj.errors
                return JsonResponse(back_dic)
            elif len(web_code) != 6:
                back_dic["status_code"] = 0
                form_obj.errors["code"] = ["验证码必须为6位纯数字", ]
                back_dic["msg"] = form_obj.errors
                return JsonResponse(back_dic)

            phone = request.POST.get("phone")
            redis_code = cache.get(phone)
            if not redis_code:
                back_dic["status_code"] = 0
                form_obj.errors["code"] = ["验证码失效", ]
                back_dic["msg"] = form_obj.errors
                return JsonResponse(back_dic)

            if redis_code != web_code:
                back_dic["status_code"] = 0
                form_obj.errors["code"] = ["验证码错误", ]
                back_dic["msg"] = form_obj.errors
                return JsonResponse(back_dic)

            data = form_obj.cleaned_data

            file_obj = request.FILES.get("avatar_file")
            if file_obj:
                data["avatar"] = file_obj
            data["username"] = phone
            print('写入用户')
            models.UserInfo.objects.create_user(**data)
            back_dic["url"] = reverse("home")
            return JsonResponse(back_dic)

        else:
            back_dic["status_code"] = 0
            back_dic["msg"] = form_obj.errors
            return JsonResponse(back_dic)


# 登陆
class Login(View):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        back_dic = {
            "status_code": 1,
            "msg": "登陆成功",
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            back_dic["url"] = reverse("home")
            return JsonResponse(back_dic)
        back_dic["status_code"] = 0
        back_dic["msg"] = "账号或者密码错误"
        return JsonResponse(back_dic)


class LoginPhone(View):
    def get(self, request):
        return render(request, "login_phone.html", locals())

    def post(self, request):
        print("run login phone")
        back_dic = {
            "status_code": 0,
            "msg": ""
        }
        phone = request.POST.get("phone")
        print("login phone:", phone)
        if not phone:
            back_dic["msg"] = "手机号不能为空"
            return JsonResponse(back_dic)
        elif not re.match(r'^1[3-9]\d{9}$', phone):
            back_dic["msg"] = "手机号有误"
            return JsonResponse(back_dic)
        elif not models.UserInfo.objects.filter(phone=phone):
            back_dic["msg"] = "手机号未注册"
            return JsonResponse(back_dic)

        code = request.POST.get("code")
        redis_code = cache.get(phone)

        print(phone, code)

        if not redis_code:
            back_dic["msg"] = "验证码失效"
            return JsonResponse(back_dic)
        elif len(code) != 6:
            back_dic["msg"] = "验证码必须为6位纯数字"
            return JsonResponse(back_dic)
        elif code != redis_code:
            back_dic["msg"] = "验证码错误"
            return JsonResponse(back_dic)

        # user = models.UserInfo.objects.filter(phone=phone).first()
        user = auth.authenticate(phone=phone)
        auth.login(request, user)
        back_dic["status_code"] = 1
        back_dic["msg"] = "登陆成功"
        back_dic["url"] = reverse("home")
        return JsonResponse(back_dic)


def logout(request):
    auth.logout(request)
    return JsonResponse({
        "1": '1'
    })


class Site(View):
    def get(self, request, username, *args, **kwargs):
        print('run 用户主页')
        user_obj = models.UserInfo.objects.filter(username=username).first()
        blog = user_obj.blog
        article_list = article_models.Article.objects.filter(blog=blog)
        print(kwargs)

        article_num = article_models.Article.objects.filter(blog=blog).count()

        tag_list = article_models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values_list("name", 'c',
                                                                                                         'pk')
        category_list = article_models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list(
            "name",
            'c',
            'pk')
        date_list = article_models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("create_time")).values(
            "month").annotate(c=Count("pk")).values_list("month", "c")

        if kwargs:
            condition = kwargs.get("condition")
            param = kwargs.get("param")
            if condition == "tag":
                article_list = article_list.filter(tag__pk=param)
            elif condition == "category":
                article_list = article_list.filter(category__pk=param)
            elif condition == "site":
                pass
            else:
                print(param)

                year, month = param.split("-")
                article_list = article_list.filter(create_time__year=year, create_time__month=month)

        return render(request, 'user_site.html', locals())


class UserBackVIew(View):
    # @login_required
    def get(self, request, condition):
        # (?P<condition>article|userinfo|other)
        print('run 后台')
        if condition == 'article':
            blog = models.UserInfo.objects.filter(pk=request.user.pk).first().blog
            article_list = article_models.Article.objects.filter(blog=blog).order_by('-create_time')

            # 用户想访问的当前页面
            current_page = request.GET.get('page', 1)
            # 用户总条数
            all_count = article_list.count()
            page_obj = Pagination(current_page=current_page, all_count=all_count)
            # 对数据进行切分
            page_queryset = article_list[page_obj.start:page_obj.end]

            return render(request, 'user_back_article.html', locals())
        elif condition == 'userinfo':
            return render(request, 'user_back_userinfo.html', locals())
        else:
            return render(request, 'user_back_other.html', locals())

    def post(self, request, condition):
        print('run userinfo')
        data = request.POST
        print(111, data)
        jx3_name = data.get("jx3_name")
        desc = data.get("desc")
        avatar_obj = request.FILES.get("avatar")

        user_obj = request.user

        user_obj.jx3_name = jx3_name
        user_obj.desc = desc

        if avatar_obj:
            user_obj.avatar = avatar_obj
        user_obj.save()

        path = request.META.get('HTTP_REFERER')
        return redirect(path)


class ArticleDetailed(View):
    def get(self, request, username, article_id):
        print(username, article_id)
        article_obj = article_models.Article.objects.filter(pk=article_id).first()

        user_obj = models.UserInfo.objects.filter(username=username).first()
        blog = user_obj.blog
        tag_list = article_models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values_list("name", 'c',
                                                                                                         'pk')
        category_list = article_models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list(
            "name",
            'c',
            'pk')
        date_list = article_models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("create_time")).values(
            "month").annotate(c=Count("pk")).values_list("month", "c")

        comment_list = article_models.Comment.objects.filter(article_id=article_id)

        return render(request, 'article_detailed.html', locals())


class SetPassword(View):
    def get(self, request):
        return render(request, 'set_password.html')

    def post(self, request):

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # 先判断旧密码是否正确
        res = request.user.check_password(old_password)
        if res:
            # 再来比对新密码是否一致
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                return redirect(reverse('login'))
            msg = '两次密码不一致'
            return render(request, 'set_password.html', {"msg": msg})
        msg = '旧密码错误'
        return render(request, 'set_password.html', {"msg": msg})
