"""Vtc user api"""

from rest_framework import viewsets
from .serializers import CustomUserSerializer, VideoLinkSerializer
from .models import CustomUser, VideoLink


class CustomUserViewSet(viewsets.ModelViewSet):
    """
        CustomUserViewSet class
        :param viewsets.ModelViewSet A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions.
        :type serializer_class: class: `CustomUserSerializer`
        :type queryset: class: `Queryset`
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class VideoLinkViewSet(viewsets.ModelViewSet):
    """
        VideoLinkViewSet class
        :param viewsets.ModelViewSet A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions.
        :type serializer_class: class: `VideoLinkSerializer`
        :type queryset: class: `Queryset`
    """
    serializer_class = VideoLinkSerializer
    queryset = VideoLink.objects.all()
