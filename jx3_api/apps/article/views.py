from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from . import models
from user import models as user_models
from django.http import JsonResponse
from django.db.models import Count, F
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from bs4 import BeautifulSoup
from django.db import transaction



class UpOrDown(View):
    def post(self, request):
        back_dic = {
            "status_code":0,
            "msg":""
        }

        is_up = int(request.POST.get("is_up"))
        article_id = request.POST.get("article_id")

        if not request.user.is_authenticated:
            back_dic["msg"] = "请先登录(右上角登录)"
        else:
            user_id = request.user.pk
            article_obj = models.Article.objects.filter(pk=article_id).first()
            if article_obj.blog.userinfo == request.user:
                if is_up:
                    back_dic["msg"] = "不能点赞自己的文章"
                else:
                    back_dic["msg"] = "不能点踩自己的文章"

            else:
                msg = models.UpOrDown.objects.filter(article_id=article_id, user=request.user).first()
                if msg:
                    if msg.is_up:
                        back_dic["msg"] = "你已经点过赞了"
                    else:
                        back_dic["msg"] = "你已经点过踩了"
                else:
                    models.UpOrDown.objects.create(is_up=is_up, user=request.user, article_id=article_id)
                    if is_up:
                        models.Article.objects.filter(pk=article_id).update(up_num=F("up_num") + 1)
                        back_dic["msg"] = "点赞成功"
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_num=F("down_num") + 1)
                        back_dic["msg"] = "点踩成功"
                    back_dic["status_code"] = 1
        return JsonResponse(back_dic)



class DeleteArticle(View):
    def get(self, request):
        print('run delete')
        article_id = request.GET.get("article_id")
        models.Article.objects.filter(pk=article_id).delete()
        return redirect('http://api.jx3blog.cn:8000/user/backend/2/')



class AddArticle(View):
    # @login_required
    def get(self, request):
        blog = user_models.UserInfo.objects.filter(pk=request.user.pk).first().blog
        category_list = models.Category.objects.filter(blog=blog)
        return render(request, 'add_article.html', locals())

    # @login_required
    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get("desc")
        content = request.POST.get('content')
        tag = request.POST.get("tag")
        category = request.POST.get("category")

        # 将需要处理的文本内容交由该模块生一个soup对象
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all()
        for tag1 in tags:
            if tag1.name == 'script':
                # 将script删除
                tag1.decompose()  # 1.解决xss攻击问题

        # 文章简介
        if not desc:
            desc = soup.text[0:150]  # 2.解决了文章简介的问题

        # 保存到数据库中
        models.Article.objects.create(title=title, content=str(soup), desc=desc,
                                                            blog=request.user.blog)

        blog = user_models.UserInfo.objects.filter(pk=request.user.pk).first().blog
        if tag:
            tag_list = tag.split(',')
            for tag in tag_list:
                print("tag了一次")
                models.Tag.objects.create(name=tag,blog=blog)
        models.Category.objects.create(name=category, blog=blog)

        return redirect('http://api.jx3blog.cn:8000/user/backend/article/')



class EditArticle(View):
    # @login_required
    def get(self, request,article_id):
        article_obj = models.Article.objects.filter(pk=article_id).first()
        blog = user_models.UserInfo.objects.filter(pk=request.user.pk).first().blog
        category_list = models.Category.objects.filter(blog=blog)

        tag_list = models.Tag.objects.filter(blog=blog)
        tags=[]

        for tag in tag_list:
            tags.append(tag.name)
        tags = ' '.join(tags)

        return render(request, 'edit_article.html', locals())

    # @login_required
    def post(self, request, article_id):
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag = request.POST.get("tag")
        category = request.POST.get("category")

        # 将需要处理的文本内容交由该模块生一个soup对象
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                # 将script删除
                tag.decompose()  # 1.解决xss攻击问题

        # 文章简介
        desc = soup.text[0:150]  # 2.解决了文章简介的问题

        # 保存到数据库中
        models.Article.objects.filter(pk=article_id).update(title=title, content=str(soup), desc=desc, blog=request.user.blog)

        blog = user_models.UserInfo.objects.filter(pk=request.user.pk).first().blog

        print(tag)
        if tag:
            l = []
            tag_list = tag.split(' ')

            for tag in tag_list:
                if tag:
                    l.append(tag)
                # models.Tag.objects.create(name=tag,blog=blog)
            set_l = set(l)


            old_tag_list = models.Tag.objects.filter(blog=blog)
            old_tags = []

            for tag in old_tag_list:
                old_tags.append(tag.name)

            set_old_tags = set(old_tags)
            print("set_l", set_l, type(set_l))
            print("set_old_tags:", set_old_tags,type(set_old_tags))
            res = set_l - set_old_tags
            for i in res:
               models.Tag.objects.create(name=i, blog=blog)


            print(res)

            res1 = set_old_tags - set_l
            for i in res1:
                models.Tag.objects.filter(name=i).delete()

            print(res1)

        models.Category.objects.update(name=category, blog=blog)

        return redirect('http://api.jx3blog.cn:8000/user/backend/article/')




class UploadImg(View):
    def post(self,request):
        # 将用户上传的图片存入media文件夹以便后续查找
        print(request.FILES)
        file_obj = request.FILES.get('imgFile')
        # 将该文件存入media文件夹
        # 1 手动拼接文件存放的路径
        path = os.path.join(settings.BASE_DIR, 'media', 'article_img')
        # 判断当前路径文件夹是否存在，不存在自动创建
        if not os.path.exists(path):
            os.mkdir(path)  # 自动创建文件夹

        file_path = os.path.join(path, file_obj.name)
        # 文件操作读写
        with open(file_path, 'wb') as f:
            for line in file_obj:
                f.write(line)
        back_dic = {
            "error": 0,
            "url": "/media/article_img/%s" % file_obj.name
        }
        return JsonResponse(back_dic)




class Comment(View):
    def post(self, request):
        back_dic = {'code': 1, 'msg': ''}
        # 获取前端发送过来的数据
        article_id = request.POST.get("article_id")
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        # 1.校验当前用户是否登录
        if request.user.is_authenticated:
            with transaction.atomic():
                # 在文章表中将普通的评论字段加1
                models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
                # 在去评论表存储真正的数据
                models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                              parent_id=parent_id)
            back_dic['msg'] = '评论成功'
        else:
            back_dic['code'] = 0
            back_dic['msg'] = '请先登录'
        return JsonResponse(back_dic)
