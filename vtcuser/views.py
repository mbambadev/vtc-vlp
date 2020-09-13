"""VTC user video link posted app views."""
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins

from notifications.signals import notify

from .permissions import IsOwnerOrReadOnly
from .models import VideoLink
from .forms import VideoLinkModelForm
from .serializers import VideoLinkSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Show all videos link
@login_required
def saved_videos(request):
    """This view show all posted videos"""
    context = dict()
    context['meta_keyword'] = context['head_title'] = context['page_head_title'] = _('My videos links')
    context['meta_description'] = _(
        'List of all saved videos'
    )
    queryset = VideoLink.objects.all()
    context['videos_links'] = queryset.filter(poster=request.user.member)
    context['unread_count']: request.user.notifications.unread().count()
    context['notifications']: request.user.notifications.all()
    return render(
        request,
        template_name='vtcuser/saved_videos_list.html',
        context=context,
    )


# View to add and update video link
@login_required
def video_crud(request, video_link_pk=None):
    """This view add and edit video link"""
    data = dict()
    instance = None
    update = False

    data['reverse_url'] = reverse('vtcuser:video_add', )

    # Notifications
    swa_messages = {
        'title': _("Videos links manager"),
        'text': _("New link video added"),
        'icon': "success",
        'button': _('Terminer')
    }

    if video_link_pk:
        instance = get_object_or_404(VideoLink, pk=video_link_pk)
        data['reverse_url'] = reverse(
            'vtcuser:video_edit',
            kwargs={
                'video_link_pk': instance.id,
            }
        )
        update = True
        swa_messages['text'] = _(
            "the video link: [%s] data update" % instance.name)

    if request.method == 'POST':
        if video_link_pk:
            instance = get_object_or_404(VideoLink, pk=video_link_pk)
            form = VideoLinkModelForm(request.POST, request.FILES, request=request,  instance=instance)
        else:
            form = VideoLinkModelForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            new_video_link = form.save(commit=False)
            new_video_link.poster = request.user.member
            new_video_link.save()

            queryset = VideoLink.objects.all()
            videos_links = queryset.filter(poster=request.user.member)
            data['form_is_valid'] = True
            data['messages'] = swa_messages
            if video_link_pk:
                verb = 'video link name: %s updated by his author'
            else:
                verb = 'New video link created'
            notify.send(sender=request.user, recipient=request.user, verb=verb)

            data['html_list'] = render_to_string(
                'includes/partial_videos_links_list.html',
                {'videos_links': videos_links},
                request=request,
            )

        else:
            data['form_is_valid'] = False
    else:
        if video_link_pk:
            form = VideoLinkModelForm(request=request, instance=instance)
        else:
            form = VideoLinkModelForm(request=request)

    context = {
        'form': form,
        'url': data['reverse_url'],
        'instance': instance,
        'update': update,
    }

    data['html_form'] = render_to_string(
        'includes/video_link_create_form.html',
        context,
        request=request,
    )
    return JsonResponse(data, content_type="application/json")


# View to delete video link
@login_required
def video_delete(request, video_link_pk):
    """This view Delete video link"""
    get_object = get_object_or_404(VideoLink, pk=video_link_pk)
    reverse_url = reverse(
        "vtcuser:video_delete",
        kwargs={'video_link_pk': video_link_pk}
    )
    data = dict()
    swa_messages = {
        'title': _('Video link deleter manager'),
        'text': _('Link of video deleted'),
        'icon': "success",
        'button': _('Close')
    }
    if request.method == 'POST':
        get_object.delete()
        data['form_is_valid'] = True
        data['messages'] = swa_messages
        queryset = VideoLink.objects.all()
        videos_links = queryset.filter(poster=request.user.member)
        data['html_list'] = render_to_string(
            'includes/partial_videos_links_list.html',
            {'videos_links': videos_links},
            request=request,
        )
    else:
        context = {
            'instance': get_object,
            'url': reverse_url
        }
        data['html_form'] = render_to_string('includes/video_link_delete.html', context, request=request)
    return JsonResponse(data)


class VideoLinkApiView(APIView):
    """
        VideoLinkApiView class
        :param class: `APIView`
        :type class: `APIView`
    """
    def get(self, request) -> Response:
        """
            This get function
            :param request: Current request
            :return class: `Response`
            :rtype class: `Response`
        """
        all_videos_links = VideoLink.objects.all().values()

        return Response({"Message": "List of videos links", "Videos links List": all_videos_links})

    def post(self, request) -> Response:
        """
            This get function
            :param request: Current request
            :return class: `Response`
            :rtype class: `Response`
        """
        VideoLink.objects.create(name=request.data["name"], link=request.data['link'], poster=request.data["poster"])

        vl = VideoLink.objects.all().filter(id=request.data["id"]).values()

        return Response({"Message": "New Link Added!", "VideoLink": vl})


class VideoLinkAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """
        VideoLinkPostRudView class
        :param class: `generics.RetrieveUpdateDestroyAPIView`
        :type class: `generics.RetrieveUpdateDestroyAPIView`
    """
    lookup_field = 'pk'
    serializer_class = VideoLinkSerializer
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        qs = VideoLink.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__icontains=query).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user.member)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VideoLinkPostRudView(generics.RetrieveUpdateDestroyAPIView):
    """
        VideoLinkPostRudView class
        :param class: `generics.RetrieveUpdateDestroyAPIView`
        :type class: `generics.RetrieveUpdateDestroyAPIView`
    """
    lookup_field = 'pk'
    serializer_class = VideoLinkSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_queryset(self):
        return VideoLink.objects.all()
