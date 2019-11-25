from django.db import models




# 陪打表
class PlayerInfo(models.Model):
    user = models.OneToOneField('user.UserInfo', on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='对应用户')
    is_keep_play = models.IntegerField(choices=((0, "否"), (1, "是")), default=0, verbose_name='是否是陪玩')
    age = models.CharField(max_length=64,null=True, verbose_name='年龄')
    is_working = models.IntegerField(choices=((0, "否"), (1, "是")), default=1, verbose_name='待业与否', blank=True)
    sex = models.IntegerField(choices=((0, "女"), (1, "男"), (2, "保密")), verbose_name='性别')
    voice = models.FileField(upload_to="keep_play_voices/", null=True, verbose_name='录音')
    price = models.CharField(max_length=32, verbose_name='计价标准')
    work_time = models.CharField(max_length=64, verbose_name='接单时间段')
    work_num = models.IntegerField(verbose_name='接单数', default=0, blank=True)
    jjc_score = models.CharField(max_length=64, verbose_name='jjc分数')
    is_skill = models.IntegerField(choices=((0, "否"), (1, "是")), verbose_name='技术与否')  # 技术与否
    is_humor = models.IntegerField(choices=((0, "否"), (1, "是")), verbose_name='幽默与否')  # 幽默与否
    accouter_num = models.CharField(max_length=64,verbose_name="装分")
    body = models.CharField(max_length=64, verbose_name='职业体型')
    addr = models.CharField(max_length=64, verbose_name="区服")
    contact_way = models.CharField(max_length=255, verbose_name=' 联系方式')

    class Meta:
        verbose_name_plural = '陪打表'


    def __str__(self):
        return self.user.jx3_name

class PlayerComment(models.Model):
    user = models.ForeignKey(to="user.UserInfo", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                             verbose_name='用户表')
    player = models.ForeignKey(to="PlayerInfo", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                                verbose_name='陪玩表')
    create_time = models.DateField(auto_now_add=True, verbose_name='评论时间')

    content = models.CharField(max_length=64, verbose_name='评论内容')
    parent = models.ForeignKey(to="self", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                               verbose_name='回复哪条评论', blank=True)




# 卖唱表
# class Sing(models.Model):
#     user = models.ForeignKey(to="UserInfo")
#     is_working = models.BooleanField()
#     sex = models.IntegerField(choices=((0, "女"), (1, "男"), (2, "保密")))
#     voice = models.FileField(upload_to="keep_play_voices/", null=True)
#     video = models.FileField(upload_to="keep_play_video/", null=True)
#     price = models.CharField(max_length=32)
#     work_time = models.CharField(max_length=64)
#     style = models.CharField(max_length=64)
#     good_at = models.CharField(max_length=64)
#     song_list = models.CharField(max_length=255)
#     work_num = models.IntegerField()
#     contact_way = models.CharField(max_length=255)
