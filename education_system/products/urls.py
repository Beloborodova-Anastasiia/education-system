from django.urls import path

from .views import lessons, lessons_in_product, statistics, purchase, LessonsViewSet

from rest_framework import routers
from django.urls import include

app_name = 'products'
router = routers.DefaultRouter()
router.register(
    r'lessons',
    LessonsViewSet,
    basename='lessons'
)

urlpatterns = [
    path('', include(router.urls)),

    # path('lessons/', lessons, name='lessons_list'),
    # path(
    #     'lessons_in_product/<str:id>/',
    #     lessons_in_product,
    #     name='lessons_in_product'
    # ),
    path('statistics/', statistics, name='statistics'),
    path('purchase/<str:id>/', purchase, name='purchase'),
]
