from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
from article import models as article_models
from utils.home_article_pages import Pagination



class HomeAPIView(View):
    def get(self, request):
        username = "输诚"
        avatar = 'default.png'

        # 3条热门文章
        hot_article_list = article_models.Article.objects.order_by('-look_num')[:3]
        print(hot_article_list)

        article_list = article_models.Article.objects.all()

        # 用户想访问的当前页面
        current_page = request.GET.get('page', 1)
        # 用户总条数
        all_count = article_list.count()
        page_obj = Pagination(current_page=current_page, all_count=all_count)
        # 对数据进行切分
        page_queryset = article_list[page_obj.start:page_obj.end]

        return render(request, 'home.html', locals())

import os

class ErrorView(View):
    def get(self,request):
        # print(request.META)
        zdc= 'http://api.jx3blog.cn:8000'
        path = os.path.join(zdc, request.META.get("PATH_INFO"))


        return render(request, "error.html",locals())


