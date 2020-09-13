"""Vtcuser forms app"""
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from .models import VideoLink, CustomUser


class VideoLinkModelForm(forms.ModelForm):
    """This is VideoLinkModelForm class."""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VideoLinkModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = VideoLink
        fields = ['name', 'link']


class VTCUserSignupModelForm(forms.ModelForm):
    """Custom user signup form class"""
    class Meta:
        model = get_user_model()
        fields = ['last_name', 'username', 'email']

    def signup(self, request, user):
        user.last_name = self.cleaned_data['last_name']

        user.save()
