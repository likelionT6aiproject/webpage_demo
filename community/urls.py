from django.urls import path
from community.views import ArticleListView, articleUpdateView, articleDeleteView
from . import views

app_name = 'community'

urlpatterns = [
    path('list', ArticleListView.as_view(), name='article_list'),
    path('create/', views.articleCreate.as_view(), name='article_create'), 
    path('<int:pk>/', views.articleDetail.as_view(), name='article_detail'), 
    path('<int:pk>/update/', articleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/delete/', articleDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]

