from django.urls import include, path
from rest_framework import routers

# from .views import LessonViewSet, ProductViewSet
from .views import lessons, products, statistics, ProductViewSet

app_name = 'products'
router = routers.DefaultRouter()
# router.register(
#     'lessons',
#     LessonViewSet,
#     basename='lessons'
# )
router.register(
    r'products',
    # 'products',
    ProductViewSet,
    basename='product'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('lessons/', lessons, name='lessons_list'),
    # path('products/', products)
    # path('product/<str:name>/', products, name='product'),
    path('statistics/', statistics, name='statistics')
]
