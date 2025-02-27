# Generated by Django 5.0.6 on 2024-07-16 07:41

import community.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_alter_post_options_alter_post_author_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('description', models.TextField()),
                ('stock_quantity', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(null=True)),
                ('product_img', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('seller_email', models.EmailField(max_length=254, null=True)),
                ('average_rating', models.FloatField(default=0.0)),
                ('category', models.ForeignKey(default=community.models.get_default_category_id, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='community.category')),
            ],
            options={
                'verbose_name': '상품',
                'verbose_name_plural': '상품',
            },
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
