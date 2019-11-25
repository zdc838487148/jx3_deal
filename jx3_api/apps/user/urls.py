from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'test/', views.test),
    path(r'register/', views.Resister.as_view(), name="register"),
    path(r'register/phone/', views.RegisterPhone.as_view(), name="register_phone"),
    path(r'sms/', views.Sms.as_view(), name='sms'),
    path(r'login/', views.Login.as_view(), name="login"),
    path(r'login/phone/', views.LoginPhone.as_view(), name="login_phone"),
    path(r'logout', views.logout, name="logout"),

    re_path(r'backend/(?P<condition>article|userinfo|other)/', views.UserBackVIew.as_view()),

    re_path(r'(?P<username>.+)/article/(?P<article_id>\d+)/', views.ArticleDetailed.as_view()),
    # re_path(r'(?P<username>.+)/', views.UserSite.as_view()),
    re_path(r'(?P<username>\w+)/(?P<condition>tag|category|archive|site)/(?P<param>[\d|-]+)/', views.Site.as_view()),
    path(r'setpassword', views.SetPassword.as_view(), name='setpassword'),



]