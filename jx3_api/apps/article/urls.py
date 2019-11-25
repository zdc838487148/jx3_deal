from django.urls import path, re_path
from . import views

urlpatterns = [
    # path(r'test/', views.test),

    path(r'updown/', views.UpOrDown.as_view(), name='up_or_down'),
    path(r'delete/', views.DeleteArticle.as_view(), name="delete_article"),
    path(r'addarticle', views.AddArticle.as_view(), name='addarticle'),
    re_path(r'editarticle/(?P<article_id>\d+)/', views.EditArticle.as_view()),
    path(r'comment', views.Comment.as_view(), name='comment'),


]