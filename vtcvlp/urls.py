"""
    Fluttercm URL Configuration
"""
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path
from django.conf.urls.static import static
from allauth.account import views as a_views
from vtcuser import views

admin.autodiscover()

urlpatterns = [
    # VTC Apps urls
    re_path(r'', include('vtcuser.urls')),
    re_path(r'^vl/api/prud/(?P<pk>d\+)/$',views.VideoLinkPostRudView.as_view(), name='vl-rud'),

    # Allauth
    re_path('account/', include('allauth.urls')),

    # allauth common url
    re_path(r"^login/$", a_views.login, name="account_login"),
    re_path(r"^logout/$", a_views.logout, {'next_page': '/'}, name="account_logout"),
    re_path(r"^registration/$", a_views.signup, name="account_signup"),
    # E-mail
    re_path(r"^email/$", a_views.email, {'next_page': '/'}, name="account_email"),
    re_path(r"^confirmation/$", a_views.email_verification_sent, name="account_email_verification_sent"),
    re_path(r"^confirmation/(?P<key>[-:\w]+)/$", a_views.confirm_email, name="account_confirm_email"),
    re_path(r"^updatepass/$", a_views.password_change, name="account_change_password"),
    re_path(r"^passwordset/$", a_views.password_set, name="account_set_password"),
    # password reset
    re_path(r"^forgetpass/$", a_views.password_reset, name="account_reset_password"),
    re_path(r"^resetpass/$", a_views.password_reset_done, name="account_reset_password_done"),
    re_path(
        r"^resetpass/cle-(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        a_views.password_reset_from_key, name="account_reset_password_from_key"),
    re_path(
        r"^resetpass/cle/ok/$",
        a_views.password_reset_from_key_done, name="account_reset_password_from_key_done"),
    # Notification app
    re_path(r'', include('notifications.urls', namespace='notifications')),
    # Admin interface
    re_path(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
