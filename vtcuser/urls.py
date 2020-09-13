"""
Vtc users app urls Configuration
"""
# -*- coding: utf-8 -*-
from django.urls import re_path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import VideoLinkViewSet
from rest_framework_jwt.views import obtain_jwt_token
router = DefaultRouter()  # add this

app_name = 'vtcuser'

router.register(r'videoslinks', VideoLinkViewSet, basename='videoslinks')

urlpatterns = [
    # Video link url
    re_path(r'^$', views.saved_videos, name='home_video_list'),
    re_path(r'^ap/auth/login/', obtain_jwt_token, name='api-login'),
    re_path(r'vl/api/prud/$', views.VideoLinkAPIView.as_view(), name='vl-list_create'),
    re_path(r'vl/api/prud/(?P<pk>\d+)/$', views.VideoLinkPostRudView.as_view(), name='vl-rud'),
    re_path(r'api/', include(router.urls)),
    re_path(r'saved/videos/list/$', views.saved_videos, name='video_list'),
    re_path(r'video/add/$', views.video_crud, name='video_add'),
    re_path(r'video/update/(?P<video_link_pk>\d+)/$', views.video_crud, name='video_edit'),
    re_path(r'video/delete/(?P<video_link_pk>\d+)/$', views.video_delete, name='video_delete'),

]