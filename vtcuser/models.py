"""Custom user module."""
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


@python_2_unicode_compatible
class CustomUser(models.Model):
    """
        Custom User class
        :param models.Model: models.Model class;
        :type user: User;
    """
    user = models.OneToOneField(User, verbose_name=_('Member'), on_delete=models.CASCADE, related_name='member')

    def __str__(self):
        """
            Dundored method return Object user presentation
        """
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """Callable function for create user profile when create account
            :param kwargs: Any other param
            :type kwargs: dict
            :param sender: User object
            :type sender: User Object
            :param instance: CustomUser
            :type instance: CustomUser object
            :param created: Return True if creation else return False
            :type created: bool: True or False
            :return None
            :rtype None object
        """
        if created:
            CustomUser.objects.create(user=instance)

    class Meta:
        """
            Class object Meta
            :type verbose_name: str, default="VTC member"
            :type verbose_name_plural: str, default="VTC members"
        """
        verbose_name = _('VTC member')
        verbose_name_plural = _('VTC members')


@python_2_unicode_compatible
class VideoLink(models.Model):
    """
        VideoLink object
        :param models.Model: models.Model class
        :type: name: str, required
        :type link: Url object, required
        :type date_add: DateTime object, default;
    """
    name = models.CharField(_('Name of video'), max_length=30)
    link = models.URLField(_('Link of the video'))
    date_add = models.DateTimeField(_('Date added'), auto_now_add=True)
    poster = models.ForeignKey(CustomUser, verbose_name='Sender', on_delete=models.CASCADE, null=True)

    def __str__(self):
        """
            Return str presentation VideoLink class
            :return name: str
        """
        return self.name

    class Meta:
        """
            Class object Meta
            :type verbose_name: str, default="Video Link"
            :type verbose_name_plural: str, default="Videos links"
        """
        verbose_name = _('Video Link')
        verbose_name_plural = _('Videos links')