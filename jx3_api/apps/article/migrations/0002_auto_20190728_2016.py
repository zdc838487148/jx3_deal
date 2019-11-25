# Generated by Django 2.2.3 on 2019-07-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': '文章表'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name_plural': '站点表'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '分类表'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': '评论表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签表'},
        ),
        migrations.AlterModelOptions(
            name='tag2article',
            options={'verbose_name_plural': '标签/文章关联'},
        ),
        migrations.AlterModelOptions(
            name='upordown',
            options={'verbose_name_plural': '点赞/踩表'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='site_title',
            field=models.CharField(default='这个人太懒了，什么都没有留下', max_length=64, verbose_name='站点个签'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='theme',
            field=models.CharField(max_length=64, null=True, verbose_name='站点css样式'),
        ),
    ]
