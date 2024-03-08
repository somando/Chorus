# Generated by Django 5.0.2 on 2024-03-07 15:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SNS', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postdata',
            old_name='music',
            new_name='music_id',
        ),
        migrations.AddField(
            model_name='postdata',
            name='album_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postdata',
            name='artist_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postdata',
            name='image',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postdata',
            name='song_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]