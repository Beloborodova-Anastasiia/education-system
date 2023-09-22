from django.urls import path

from .views import lessons, lessons_in_product, purchase, statistics

urlpatterns = [
    path('lessons/', lessons, name='lessons_list'),
    path(
        'lessons_in_product/<str:id>/',
        lessons_in_product,
        name='lessons_in_product'
    ),
    path('statistics/', statistics, name='statistics'),
    path('purchase/<str:id>/', purchase, name='purchase'),
]
