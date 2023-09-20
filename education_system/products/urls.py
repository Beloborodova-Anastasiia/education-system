from django.urls import include, path
from rest_framework import routers

# from .views import LessonViewSet, ProductViewSet
from .views import lessons, products

# app_name = 'products'
# router = routers.DefaultRouter()
# router.register(
#     'lessons',
#     LessonViewSet,
#     basename='lessons'
# )
# router.register(
#     'products',
#     ProductViewSet,
#     basename='products'
# )

urlpatterns = [
    # path('', include(router.urls)),
    path('lessons/', lessons, name='lessons_list'),
    # path('products/', products)
    path('<str:name>/', products, name='product'),
]
