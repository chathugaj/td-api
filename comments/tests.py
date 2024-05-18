from django.contrib.auth.models import User

from posts.models import Post
from .models import Comment
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='pass')

    def test_can_list_comment(self):
        user = User.objects.get(username='user')
        post = Post.objects.create(owner=user, title='Test post')
        Comment.objects.create(owner=user, content='Test comment', post=post)
        response = self.client.get('/comments/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment_response = self.client.post('/comments/', { 'content': 'Test comment', 'post': 1 })
        self.assertEqual(comment_response.status_code, status.HTTP_201_CREATED)

        count = Comment.objects.count()
        self.assertEqual(count, 1)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/comments/', {'content': 'Test comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class PostDetailViewTests(APITestCase):
#     def setUp(self):
#         user = User.objects.create_user(username='user', password='pass')
#         johan = User.objects.create_user(username='johan', password='pass')
#         Post.objects.create(
#             owner=user, title='a title', body='test user content'
#         )
#         Post.objects.create(
#             owner=johan, title='another title', body='johans content'
#         )
#
#     def test_can_retrieve_post_using_valid_id(self):
#         response = self.client.get('/posts/1/')
#         self.assertEqual(response.data['title'], 'a title')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_cant_retrieve_post_using_invalid_id(self):
#         response = self.client.get('/posts/500/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_user_can_update_own_post(self):
#         self.client.login(username='user', password='pass')
#         response = self.client.put('/posts/1/', {'title': 'a new title'})
#         post = Post.objects.filter(pk=1).first()
#         self.assertEqual(post.title, 'a new title')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_user_cant_update_another_users_post(self):
#         self.client.login(username='user', password='pass')
#         response = self.client.put('/posts/2/', {'title': 'a new title'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)