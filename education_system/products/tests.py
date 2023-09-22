
# from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# # from .models import Account
from unittest import TestCase
from django.test import Client

# # class StatisticsTests(APITestCase):
# #     def test_statistics(self):
# #         """
# #         Ensure all users can see statistics.
# #         """
# #         url = reverse('api/statistics')
# #         # data = {'name': 'DabApps'}
# #         # response = self.client.post(url, data, format='json')
# #         response = self.client.get(url, format='json')
# #         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #         # self.assertEqual(Account.objects.count(), 1)
# #         # self.assertEqual(Account.objects.get().name, 'DabApps')
# # education_system.settings.configure()



class ExampleTestCase(TestCase):
    def setUp(self):
        self.relative_path = '/api/'
        self.client = Client()

    def call_api(self, endpoint):
        return self.client.get(self.relative_path + endpoint)

    def test_product_types_retrieve(self):
        response = self.call_api('statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#     # def test_requires_different_path(self):
#     #     # self.relative_path = '/api/api_product/v1/'
#     #     response = self.call_api('product_types/')
