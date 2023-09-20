from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Lesson, Product, UserLesson, UserProduct
from .serializers import (LessonSerializer, ProductSerializer,
                          )

User = get_user_model()


@api_view(['GET'])
def lessons(request):
    # user = User.objects.filter(id=1)
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products(request, name):
    user = request.user
    product = get_object_or_404(Product, name=name)
    if UserProduct.objects.filter(product=product, user=user).exists():
        lessons = product.lessons.all()
        # user_products = UserProduct.objects.filter(user=user)
        # products = Product.objects.filter(
        #     id__in=user_products.values_list('product',)
        # ).all()
        # lessons = Lesson.objects.filter(
        #     id__in=products.values_list('lessons',)
        # )
    # serializer = ProductSerializer(product, context={'request': request})
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    else:
        return Response(
            'У вас нет доступа к этому продукту',
            status=status.HTTP_403_FORBIDDEN
        )


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
