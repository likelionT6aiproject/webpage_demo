# Generated by Django 5.0.4 on 2024-07-24 05:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_article_delete_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='community_like',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
