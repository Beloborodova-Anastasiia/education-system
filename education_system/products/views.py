from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Lesson, Product, UserLesson, UserProduct
from .serializers import (LessonSerializer, ProductSerializer,
                          UserProductSerializer)

User = get_user_model()


@api_view(['GET'])
def lessons(request):
    # user = User.objects.filter(id=1)
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products(request):
    user = request.user
    user_products = UserProduct.objects.filter(user=user)
    print(user_products)
    products = Product.objects.filter(
        id__in=user_products.values_list('product',)
    ).all()
    print(products)
    # return User.objects.all()
    # user = User.objects.filter(id=1).first()
    # products = products.user
    # ingredient_recipe = user.userproduct_set.filter(

    #         ).first()
    # products = Product.objects.all()
    # print(products)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def lessons(request):
    user = request.user
    user_products = UserProduct.objects.filter(user=user)
    products = Product.objects.filter(
        id__in=user_products.values_list('product',)
    ).all()
    lessons = Lesson.objects.filter(
        id__in=products.values_list('lessons',)
    )
    serializer = LessonSerializer(lessons, many=True, context={'request': request})
    return Response(serializer.data)

# class LessonViewSet(viewsets.ModelViewSet):
#     queryset = Lesson.objects.all()
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = LessonSerializer
#     # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
#     # filterset_class = IngredientFilter


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = ProductSerializer
#     # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
#     # filterset_class = IngredientFilter
