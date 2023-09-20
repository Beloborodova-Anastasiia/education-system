# from django.shortcuts import get_object_or_404
# from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers

from .models import (Lesson, LessonProduct, Product, UserProduct, UserLesson)


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            # 'id',
            'name',
            'link',
            'duration',
            'status'
        )

    def get_status(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if UserLesson.objects.filter(lesson=obj, user=user).exists():
            # return UserLesson.objects.filter(author=obj, user=user).status
            return "!!!"
    
#     def serialize_lesson_product(self, lesson):
#         if 'product' in self.context:
#             lesson_product = lesson.lessonproducte_set.filter(
#                 recipe=self.context['product']
#             ).first()
#             if lesson_product:
#                 return LessonProductSerializer(lesson_product).data
#         return {}

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         return {**representation, **self.serialize_lesson_product(instance)}


# class LessonProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LessonProduct
#         fields = ()


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            # 'id',
            'name',
            'owner',
            'lessons',
        )


class UserProductSerializer(serializers.ModelSerializer):
    lessons = ProductSerializer(many=True)

    class Meta:
        model = Lesson
        fields = (
            'product',
        )
