from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from .models import article, Category
from .forms import RegisterForm ,CommentForm, CommentEditForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import article,CommunityComment, article





class articleCreate(LoginRequiredMixin, FormView):

    template_name = 'register_article.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')  # 로그인 페이지의 URL

    def form_valid(self, form):
        # 로그인된 사용자의 이메일 가져오기
        email = self.request.user.email

        # 폼에서 인스턴스 생성
        product_instance = form.save(commit=False)
        product_instance.user_email = email  
        product_instance.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # 사용자가 로그인되어 있는지 확인
        if not self.request.user.is_authenticated:
            # 로그인되어 있지 않은 경우 로그인 페이지로 리디렉션
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    

from django.shortcuts import get_object_or_404
from accounts.models import CustomUser

class articleDetail(DetailView):
    model = article  
    template_name = 'article_detail.html'
    context_object_name = 'article'



#업데이트 view
class articleUpdateView(UpdateView):
    model = article
    fields = ['article_name', 'description', 'category', 'article_img']
    template_name = 'article_update.html'
    success_url = reverse_lazy('home')

#삭제 view
class articleDeleteView(DeleteView):
    model = article
    success_url = reverse_lazy('home')  # 삭제 후 이동할 URL

    # 템플릿 파일 이름 지정
    template_name = 'article_confirm_delete.html'


class ArticleListView(ListView):
    model = article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 30

    def get_queryset(self):
        # 작성 날짜를 기준으로 내림차순 정렬
        return article.objects.all().order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.get_queryset()
        paginator = Paginator(articles, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
    
    
#===========좋아요==========================

@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(article, pk=pk)
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            post.community_like += 1
            post.save()
    return redirect('community:article_detail', pk=pk)

@login_required
def unlike_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(article, pk=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.community_like -= 1
            post.save()
    return redirect('community:article_detail', pk=pk)




#=========댓글===========================================


# 댓글 추가
@login_required
def add_comment(request, pk):
    article_instance = get_object_or_404(article, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.community = article_instance
            comment.author = request.user
            comment.save()
            return redirect('community:article_detail', pk=article_instance.pk)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form, 'article': article_instance})

# 댓글 수정
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(CommunityComment, id=comment_id)
    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('community:article_detail', pk=comment.community.pk)
    else:
        form = CommentEditForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})

# 댓글 삭제
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(CommunityComment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('community:article_detail', pk=comment.community.pk)
    return render(request, 'community/delete_comment.html', {'comment': comment})

# 댓글 좋아요
@login_required
def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user not in comment.liked_by.all():
            comment.liked_by.add(request.user)
            comment.community_comment_like += 1
            comment.save()
            messages.success(request, "Comment liked.")
        return redirect('community:article_detail', pk=comment.community.pk)
    return redirect('community:article_detail', pk=comment.community.pk)

# 댓글 좋아요 취소
@login_required
def unlike_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user in comment.liked_by.all():
            comment.liked_by.remove(request.user)
            comment.community_comment_like -= 1
            comment.save()
            messages.success(request, "Comment unliked.")
        return redirect('community:article_detail', pk=comment.community.pk)
    return redirect('community:article_detail', pk=comment.community.pk)