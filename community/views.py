from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from .models import article, Category
from .forms import RegisterForm 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages



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
        product_instance.user_email = email  # 판매자 이메일 저장
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