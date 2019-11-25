# Generated by Django 2.2.3 on 2019-07-31 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PalyerInfo9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.BooleanField(verbose_name='性别')),
                ('voice', models.FileField(null=True, upload_to='player_voice/', verbose_name='声音')),
                ('addr', models.CharField(max_length=64, verbose_name='区服')),
                ('school', models.CharField(max_length=64, verbose_name='体型')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=64, null=True, verbose_name='年龄')),
                ('is_working', models.BooleanField(verbose_name='待业与否')),
                ('sex', models.IntegerField(choices=[(0, '女'), (1, '男'), (2, '保密')], verbose_name='性别')),
                ('voice', models.FileField(null=True, upload_to='keep_play_voices/', verbose_name='录音')),
                ('price', models.CharField(max_length=32, verbose_name='计价标准')),
                ('work_time', models.CharField(max_length=64, verbose_name='接单时间段')),
                ('work_num', models.IntegerField(verbose_name='接单数')),
                ('jjc_score', models.CharField(max_length=64, verbose_name='jjc分数')),
                ('is_skill', models.BooleanField(null=True, verbose_name='技术与否')),
                ('is_humor', models.BooleanField(null=True, verbose_name='幽默与否')),
                ('accouter_num', models.CharField(max_length=64, verbose_name='装分')),
                ('body', models.CharField(max_length=64, verbose_name='职业体型')),
                ('addr', models.CharField(max_length=64, verbose_name='区服')),
                ('contact_way', models.CharField(max_length=255, verbose_name=' 联系方式')),
                ('user', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='对应用户')),
            ],
        ),
    ]
