from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    create_time = models.DateField(auto_now_add=True, verbose_name='注册时间')
    jx3_name = models.CharField(max_length=16, verbose_name='昵称')
    avatar = models.FileField(upload_to="head_img/", default='head_img/default.png', null=True, verbose_name='头像')
    desc = models.CharField(max_length=255, default='这个人很懒什么都没有留下', verbose_name='个性签名')
    is_singer = models.IntegerField(choices=((0, "否"), (1, "是")), default=0, verbose_name='是否是卖唱')
    phone = models.CharField(max_length=16, null=True, verbose_name='手机号码')
