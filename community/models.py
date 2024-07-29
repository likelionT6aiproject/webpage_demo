from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # 이미지 필드 추가

    def __str__(self):
        return self.category_name
    
    # def get_absolute_url(self):
    #     return f'/category/{self.slug}/'
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'



def get_default_category_id():
    first_category = Category.objects.first()  # 첫 번째 카테고리 가져오기
    if first_category:
        return first_category.pk  # 카테고리의 ID 반환
    return None

class article(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=get_default_category_id)
    article_img = models.ImageField(upload_to='product_images/', null=True, blank=True)  #이름 수정됨
    user_email = models.EmailField(null=True)

    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)  # ManyToManyField 추가
    community_like = models.PositiveIntegerField(default=0)  # 좋아요 수를 저장할 필드
    
    
    def __str__(self):
        return self.article_name
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글'

    def save(self, *args, **kwargs):
        if self.pk:  # 인스턴스가 이미 존재하는 경우에만 updated_date 업데이트
            self.updated_date = timezone.now()
        super().save(*args, **kwargs)


class CommunityComment(models.Model):
    community = models.ForeignKey(article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    community_comment_like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author} on {self.community}'