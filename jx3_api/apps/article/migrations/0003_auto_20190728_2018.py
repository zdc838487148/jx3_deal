# Generated by Django 2.2.3 on 2019-07-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20190728_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='theme',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='站点css样式'),
        ),
    ]