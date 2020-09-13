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
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VideoLink
        fields = [
            'uri',
            'id',
            'name',
            'link',
            'poster',
        ]
        read_only_fields = ['id', 'poster']

    def get_uri(self, obj):
        return obj.get_api_url()

    def validate_name(self, value):
        """
        Validate a name of link given are uniq
        :param value: name of link to check
        :rtype str
        """
        qs = VideoLink.objects.filter(name__contains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title is already in use")
        return value