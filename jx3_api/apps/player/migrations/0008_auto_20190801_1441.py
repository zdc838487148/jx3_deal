# Generated by Django 2.2.3 on 2019-08-01 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20190801_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerinfo',
            name='voice',
            field=models.FileField(null=True, upload_to='keep_play_voices/', verbose_name='录音'),
        ),
    ]
