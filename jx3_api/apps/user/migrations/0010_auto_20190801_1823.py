# Generated by Django 2.2.3 on 2019-08-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190801_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='head_img/default.png', null=True, upload_to='head_img/', verbose_name='头像'),
        ),
    ]
