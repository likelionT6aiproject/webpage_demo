from django.contrib import admin
from .models import article, Category

 
class articleAdmin(admin.ModelAdmin):
    list_display = ('article_id','article_name')
 
admin.site.register(article, articleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    # prepopulated_fields = {'slug' : ('name',)}
 
admin.site.register(Category, CategoryAdmin)
