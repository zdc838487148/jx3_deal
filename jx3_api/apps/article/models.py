from django.db import models

# Create your models here.
class Blog(models.Model):
    site_name = models.CharField(max_length=16, verbose_name='站点名称')
    site_title = models.CharField(max_length=64, verbose_name='站点个签', default='这个人太懒了，什么都没有留下')
    theme = models.CharField(max_length=64, null=True, verbose_name='站点css样式', blank=True)

    userinfo = models.OneToOneField('user.UserInfo', db_constraint=False, on_delete=models.DO_NOTHING, null=True,
                                    verbose_name='用户信息')

    class Meta:

        verbose_name_plural = '站点表'


    def __str__(self):
        return '站点：%s' % self.site_name


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章简介')
    content = models.TextField(verbose_name="文章内容")
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    # 数据库查询优化
    look_num = models.IntegerField(default=0, verbose_name='阅读量')
    up_num = models.IntegerField(default=0, verbose_name='点赞数')
    down_num = models.IntegerField(default=0, verbose_name='点踩数')
    comment_num = models.IntegerField(default=0, verbose_name='评论数')  # 评论数

    blog = models.ForeignKey(to="Blog", on_delete=models.DO_NOTHING, db_constraint=False, null=True, verbose_name='站点表')
    category = models.ForeignKey(to="Category", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                                 verbose_name='分类表')
    tag = models.ManyToManyField(to="Tag", verbose_name='标签文章对应表')

    class Meta:
        verbose_name_plural = '文章表'


    def __str__(self):
        return '文章：%s' % self.title



# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=16, verbose_name="标签名")
    blog = models.ForeignKey(to="Blog", on_delete=models.DO_NOTHING, db_constraint=False, null=True, verbose_name='站点表')


    class Meta:
        verbose_name_plural = '标签表'


    def __str__(self):
        return '标签：%s' % self.name


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='分类名')

    blog = models.ForeignKey(to="Blog", on_delete=models.DO_NOTHING, db_constraint=False, null=True, verbose_name='站点表')

    class Meta:
        verbose_name_plural = '分类表'


    def __str__(self):
        return '分类：%s' % self.name


# 标签/文章 多对多关联表
class Tag2Article(models.Model):
    tag = models.ForeignKey(to="Tag", on_delete=models.DO_NOTHING, db_constraint=False, null=True, verbose_name='标签表')
    article = models.ForeignKey(to="Article", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                                verbose_name='文章表')

    class Meta:
        verbose_name_plural = '标签/文章关联'


    def __str__(self):
        return '标签/文章关联表'


# 点赞/踩表
class UpOrDown(models.Model):
    user = models.ForeignKey(to="user.UserInfo", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                             verbose_name='用户表')
    article = models.ForeignKey(to="Article", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                                verbose_name='文章表')

    is_up = models.BooleanField(verbose_name='点赞/点踩')


    class Meta:
        verbose_name_plural = '点赞/踩表'


    def __str__(self):
        return '点赞/踩表'

# 评论表
class Comment(models.Model):
    user = models.ForeignKey(to="user.UserInfo", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                             verbose_name='用户表')
    article = models.ForeignKey(to="Article", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                                verbose_name='文章表')
    create_time = models.DateField(auto_now_add=True, verbose_name='评论时间')

    content = models.CharField(max_length=64, verbose_name='评论内容')
    parent = models.ForeignKey(to="self", on_delete=models.DO_NOTHING, db_constraint=False, null=True,
                               verbose_name='回复哪条评论', blank=True)

    class Meta:
        verbose_name_plural = '评论表'


    def __str__(self):
        return self.user.jx3_name + self.title
