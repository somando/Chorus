# Generated by Django 5.0.2 on 2024-03-08 14:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SNS', '0003_alter_postdata_original_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]