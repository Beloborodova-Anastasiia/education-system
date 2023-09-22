
# from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse

# from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Lesson, Product, LessonProduct, UserLesson, UserProduct

User = get_user_model()




# class ExampleTestCase(TestCase):
class ExampleTestCase(APITestCase):
    @classmethod
    def setUp(cls):
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

        cls.lessons_data = {
            'name': 'first',
            'duration': 10,
            'link': 'null',
            'view_duration': 10,
            'status': 'Просмотрено'
        }

    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.get(username=self.username)

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
    
    # def test_authorized_user_access(self):
    #     response = self.client.get(self.url_lessons, **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     response = self.client.get(
    #         self.url_lessons_in_product_first,
    #         **self.bearer_token
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     response = self.client.get(self.url_statistics, **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_unauthorized_user_no_access_to_lessons(self):
    #     response = self.client.get(self.url_lessons)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     response = self.client.get(self.url_lessons_in_product_first)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_unauthorized_user_access_statistics(self):
    #     response = self.client.get(self.url_statistics)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_no_access_product_not_buy(self):
    #     response = self.client.get(
    #         self.url_lessons_in_product_sec,
    #         **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lessons_correct_result(self):
        response = self.client.get(self.url_lessons, **self.bearer_token, format='json')
        context = response.data
        print(context)


