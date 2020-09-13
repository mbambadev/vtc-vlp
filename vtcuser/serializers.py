"""VTC user app serializer"""
from rest_framework import serializers
from .models import CustomUser, VideoLink


class CustomUserSerializer(serializers.ModelSerializer):
    """
        CustomUserSerializer class
        A `ModelSerializer` is just a regular `Serializer`, except that:
        * A set of default fields are automatically populated.
        * A set of default validators are automatically populated.
        * Default `.create()` and `.update()` implementations are provided.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'


class VideoLinkSerializer(serializers.ModelSerializer):
    """
        CustomUserSerializer class
        A `ModelSerializer` is just a regular `Serializer`, except that:
        * A set of default fields are automatically populated.
        * A set of default validators are automatically populated.
        * Default `.create()` and `.update()` implementations are provided.
    """
    class Meta:
        model = VideoLink
        fields = '__all__'
