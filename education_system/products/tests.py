
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Lesson, LessonProduct, Product, UserLesson, UserProduct

User = get_user_model()


class ExampleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.username = 'User'
        cls.password = 'password'
        cls.data = {
            'username': cls.username,
            'password': cls.password
        }
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
        cls.owner = User.objects.create_user(
            username='owner',
            password='password'
        )
        cls.url_lessons = '/api/lessons/'
        cls.url_statistics = '/api/statistics/'
        cls.lesson_first = Lesson.objects.create(
            name='first',
            duration=10
        )
        cls.lesson_sec = Lesson.objects.create(
            name='second',
            duration=20
        )
        cls.lesson_third = Lesson.objects.create(
            name='third',
            duration=30
        )
        cls.product_first = Product.objects.create(
            name='First',
            owner=cls.owner,
        )
        cls.url_lessons_in_product_first = (
            '/api/lessons_in_product/' + str(cls.product_first.id) + '/'
        )
        LessonProduct.objects.create(
            lesson=cls.lesson_first,
            product=cls.product_first
        )
        cls.product_sec = Product.objects.create(
            name='Second',
            owner=cls.owner,
        )
        cls.url_lessons_in_product_sec = (
            '/api/lessons_in_product/' + str(cls.product_sec.id) + '/'
        )
        LessonProduct.objects.create(
            lesson=cls.lesson_sec,
            product=cls.product_sec
        )
        cls.product_third = Product.objects.create(
            name='Third',
            owner=cls.owner,
        )
        cls.url_lessons_in_product_third = (
            '/api/lessons_in_product/' + str(cls.product_third.id) + '/'
        )
        LessonProduct.objects.create(
            lesson=cls.lesson_third,
            product=cls.product_third
        )
        UserProduct.objects.create(
            user=cls.user,
            product=cls.product_first
        )
        cls.user_lesson = UserLesson.objects.get(
            user=cls.user,
            lesson=cls.lesson_first
        )
        cls.user_lesson.view_duration = 10
        cls.user_lesson.save()
        UserProduct.objects.create(
            user=cls.user,
            product=cls.product_sec
        )
        cls.lessons_data = {
            'name': 'first',
            'duration': 10,
            'link': 'null',
            'view_duration': 10,
            'status': 'Просмотрено'
        }

    @property
    def bearer_token(self):
        user = User.objects.get(username=self.username)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_authorized_user_access(self):
        response = self.client.get(
            self.url_lessons,
            **self.bearer_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            self.url_lessons_in_product_first,
            **self.bearer_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            self.url_statistics,
            **self.bearer_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_no_access_to_lessons(self):
        response = self.client.get(
            self.url_lessons,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(
            self.url_lessons_in_product_first,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_access_statistics(self):
        response = self.client.get(
            self.url_statistics,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_no_access_product_not_buy(self):
        response = self.client.get(
            self.url_lessons_in_product_third,
            **self.bearer_token,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lessons_correct_result(self):
        response = self.client.get(
            self.url_lessons,
            **self.bearer_token,
            format='json')
        content = response.data[0]
        self.assertEqual(len(response.data), 2)
        self.assertEqual(content['name'], self.lesson_first.name)
        self.assertEqual(content['link'], self.lesson_first.link)
        self.assertEqual(content['duration'], self.lesson_first.duration)
        self.assertEqual(content['status'], self.lessons_data['status'])
        self.assertEqual(
            content['view_duration'],
            self.user_lesson.view_duration
        )
        self.assertNotIn('view_date', content)

    def test_lessons_in_product_correct_result(self):
        response = self.client.get(
            self.url_lessons_in_product_first,
            **self.bearer_token,
            format='json')
        content = response.data[0]
        self.assertEqual(len(response.data), 1)
        self.assertEqual(content['name'], self.lesson_first.name)
        self.assertEqual(content['link'], self.lesson_first.link)
        self.assertEqual(content['duration'], self.lesson_first.duration)
        self.assertEqual(content['status'], self.lessons_data['status'])
        self.assertEqual(
            content['view_duration'],
            self.user_lesson.view_duration
        )
        self.assertEqual(
            content['view_date'], self.user_lesson.view_date)

    def test_statistics_correct_result(self):
        response = self.client.get(
            self.url_statistics,
            **self.bearer_token,
            format='json')
        content = response.data[0]
        self.assertEqual(len(response.data), 3)
        self.assertEqual(content['name'], self.product_first.name)
        self.assertEqual(content['lessons_viewed'], 1)
        self.assertEqual(content['view_time'], 10)
        self.assertEqual(content['users_count'], 1)
        self.assertEqual(content['acquisition_percentage'], 50)
