from django.contrib.auth.models import User

from posts.models import Post
from .models import Comment
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        Post.objects.create(owner=user, title='Test post')

    def test_can_list_comment(self):
        user = User.objects.get(username='user')
        post = Post.objects.get(title='Test post')
        Comment.objects.create(owner=user, content='Test comment', post=post)
        response = self.client.get('/comments/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='user', password='pass')

        post = Post.objects.get(title='Test post')
        comment_response = self.client.post('/comments/', { 'content': 'Test comment', 'post': post.id })
        self.assertEqual(comment_response.status_code, status.HTTP_201_CREATED)

        count = Comment.objects.count()
        self.assertEqual(count, 1)

    def test_user_not_logged_in_cant_create_comment(self):
        response = self.client.post('/comments/', {'content': 'Test comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        johan = User.objects.create_user(username='johan', password='pass')
        post1 = Post.objects.create(
            owner=user, title='a title', body='test user content'
        )
        post2 = Post.objects.create(
            owner=johan, title='another title', body='johans content'
        )
        Comment.objects.create(
            owner=user, post=post1, content='fancy comment'
        )
        Comment.objects.create(
            owner=johan, post=post2, content='second comment'
        )

    def test_can_retrieve_comment_using_valid_id(self):
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['content'], 'fancy comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_comment_using_invalid_id(self):
        response = self.client.get('/comments/500/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.put('/comments/1/', {'content': 'updated fancy comment'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'updated fancy comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_comment(self):
        self.client.login(username='user', password='pass')
        response = self.client.put('/comments/2/', {'content': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)