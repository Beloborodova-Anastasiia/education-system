from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Lesson, Product, UserProduct, UserLesson
from .serializers import LessonSerializer, StatisticsSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def lessons_in_product(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    if UserProduct.objects.filter(product=product, user=user).exists():
        lessons = product.lessons.all()
        serializer = LessonSerializer(
            lessons,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    else:
        return Response(
            'У вас нет доступа к этому продукту',
            status=status.HTTP_403_FORBIDDEN
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def lessons(request):
    user = request.user
    user_lessons = UserLesson.objects.filter(
        user=user
    ).select_related('lesson')
    lessons = Lesson.objects.filter(
        id__in=user_lessons.values_list('lesson',)
    )
    serializer = LessonSerializer(
        lessons,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def statistics(request):
    products = Product.objects.all()
    serializer = StatisticsSerializer(
        products,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def purchase(request, id):
    product = get_object_or_404(Product, id=id)
    user = request.user
    UserProduct.objects.create(user=user, product=product)
    return Response()


from rest_framework import filters, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import LessonFilter

class LessonsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = LessonFilter
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        user_lessons = UserLesson.objects.filter(
            user=user
        ).select_related('lesson')
        lessons = Lesson.objects.filter(
            id__in=user_lessons.values_list('lesson',)
        )
        return lessons
