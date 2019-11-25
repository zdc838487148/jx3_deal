from django.urls import path, re_path
from . import views

urlpatterns = [
    path("setplayerinfo/", views.SetPlayerInfo.as_view(), name="setplayerinfo"),
    path('playerviews/', views.PlayerView.as_view(), name="playerview"),
    re_path('playerdetail/(?P<player_id>\d+)/',views.PlayerDetail.as_view()),
    path(r'playercomment/',views.PlayerComment.as_view(), name='player_comment'),
    path('alipay/', views.AliPayAPIView.as_view(), name='alipay'),
    path('aliback/', views.AliPayBackViewSet.as_view())



]