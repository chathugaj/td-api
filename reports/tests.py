from django.contrib.auth.models import User

from .models import Report
from rest_framework import status
from rest_framework.test import APITestCase


class ReportListViewTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        johan = User.objects.create_user(username='johan', password='pass')
        User.objects.create_user(username='admin', password='pass', is_superuser=True)
        Report.objects.create(owner=user, reason='Test reason', message='Test contact message')

    def test_can_list_own_reports(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_list_others_reports(self):
        self.client.login(username='johan', password='pass')
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_superuser_can_access_reports(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_creat_report(self):
        self.client.login(username='user', password='pass')
        created = self.client.post('/reports/', {'reason': 'Test reason'})
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/reports/')
        self.assertEqual(len(response.data), 2)


class LikeDetailViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='pass')
        johan = User.objects.create_user(username='johan', password='pass')
        userReport = Report.objects.create(
            owner=user, reason='A test reason', message='test user message'
        )
        johanReport = Report.objects.create(
            owner=johan, reason='A test reason', message='test user message'
        )

    def test_cannot_retrieve_without_logging_in(self):
        response = self.client.get('/reports/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_retrieve_own_report_using_valid_id(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/reports/1/')
        self.assertEqual(response.data['reason'], 'A test reason')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_report_using_invalid_id(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/reports/500/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_retrieve_report_using_valid_id(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/reports/1/')
        self.assertEqual(response.data['reason'], 'A test reason')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

