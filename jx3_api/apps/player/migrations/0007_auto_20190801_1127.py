# Generated by Django 2.2.3 on 2019-08-01 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_playerinfo_is_keep_play'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerinfo',
            name='voice',
            field=models.FileField(null=True, upload_to='media/keep_play_voices/', verbose_name='录音'),
        ),
    ]