from django.contrib.auth.models import User

from posts  .models import Post
from .models import Like
from rest_framework import status
from rest_framework.test import APITestCase


class LikeListViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        Post.objects.create(owner=user, title='Test post')

    def test_can_list_like(self):
        user = User.objects.get(username='user')
        post = Post.objects.get(title='Test post')
        Like.objects.create(owner=user, post=post)
        response = self.client.get('/likes/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_like(self):
        self.client.login(username='user', password='pass')

        post = Post.objects.get(title='Test post')
        like_response = self.client.post('/likes/', { 'post': post.id })
        self.assertEqual(like_response.status_code, status.HTTP_201_CREATED)

        count = Like.objects.count()
        self.assertEqual(count, 1)

    def test_user_not_logged_in_cant_create_like(self):
        response = self.client.post('/likes/', {'post': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        johan = User.objects.create_user(username='johan', password='pass')
        post1 = Post.objects.create(
            owner=user, title='a title', body='test user content'
        )
        post2 = Post.objects.create(
            owner=johan, title='another title', body='johans content'
        )
        Like.objects.create(
            owner=user, post=post1
        )
        Like.objects.create(
            owner=johan, post=post2
        )

    def test_can_retrieve_like_using_valid_id(self):
        response = self.client.get('/likes/1/')
        self.assertEqual(response.data['post'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_like_using_invalid_id(self):
        response = self.client.get('/likes/500/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
