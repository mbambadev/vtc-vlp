"""vtcuser app Test"""

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from vtcuser.models import VideoLink, CustomUser
from rest_framework_jwt.settings import api_settings

encode_handler = api_settings.JWT_ENCODE_HANDLER
payload_handler = api_settings.JWT_PAYLOAD_HANDLER

User = get_user_model()


class VideoLinkApiTestCase(APITestCase):
    """VideoLinkApiTestCase class"""
    def setUp(self) -> None:
        user_obj = User(username='test_vtc_user', email='testvtc@vtc.com')
        user_obj.set_password('some_vtc_password')
        user_obj.save()

        # App member
        test_member, member_created = CustomUser.objects.get_or_create(user=user_obj)

        # Video link
        video_link = VideoLink.objects.create(
            poster=test_member,
            name='New link name',
            link='http://testlink.org/',
        )

    def test_single_user(self):
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_vl(self):
        video_link_count = VideoLink.objects.count()
        self.assertEqual(video_link_count, 1)

    def test_get_list(self):
        """Test the get list"""
        data = {}
        url = api_reverse("vtcuser:vl-list_create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item(self):
        video_link = VideoLink.objects.first()
        data = {}
        url = video_link.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {
            'name': 'New link name',
            'link': 'http://testlink.org/',
        }
        url = api_reverse("vtcuser:vl-list_create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item(self):
        video_link = VideoLink.objects.first()
        url = video_link.get_api_url()
        data = {
            'name': 'Random name title',
            'link': 'http://testlink.org/',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        vl_post = VideoLink.objects.first()
        url = vl_post.get_api_url()
        data = {'name': 'Change me now', 'link': 'http://testlink.com/'}
        user_object = User.objects.first()
        payload = payload_handler(user_object)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        user_object = User.objects.first()
        payload = payload_handler(user_object)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {'name': 'New link name 5', 'link': 'http://testlink.org/',}
        url = api_reverse("vtcuser:vl-list_create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username="test_vtc2020")
        # App member
        test_member, member_created = CustomUser.objects.get_or_create(user=owner)

        # Video link
        video_link = VideoLink.objects.create(
            poster=test_member,
            name='New link name',
            link='http://testlink.org/',
        )
        user_object = User.objects.first()
        self.assertNotEqual(user_object.username, owner.username)
        payload = payload_handler(user_object)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {'name': 'New link name 5', 'link': 'http://testlink.org/', }
        url = video_link.get_api_url()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_update(self):
        data = {
            'username': 'test_vtc_user',
            'password': 'some_vtc_password'
        }
        url = api_reverse('vtcuser:api-login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            vl_post = VideoLink.objects.first()
            url = vl_post.get_api_url()
            data = {'name': 'Change me now', 'link': 'http://testlink.com/'}

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)