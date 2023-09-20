# from django.shortcuts import get_object_or_404
# from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers

from .models import (Lesson, LessonProduct, Product, UserProduct, UserLesson)


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    viewing_duration = serializers.SerializerMethodField()
    date_viewing = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            # 'id',
            'name',
            'link',
            'duration',
            'status',
            'viewing_duration',
            'date_viewing'
        )

    def get_status(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if UserLesson.objects.filter(lesson=obj, user=user).exists():
            return UserLesson.objects.filter(
                lesson=obj, user=user
            ).first().status

    def get_viewing_duration(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if UserLesson.objects.filter(lesson=obj, user=user).exists():
            return UserLesson.objects.filter(
                lesson=obj, user=user
            ).first().viewing_duration
    
    def get_date_viewing(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if UserLesson.objects.filter(lesson=obj, user=user).exists():
            return UserLesson.objects.filter(
                lesson=obj, user=user
            ).first().date_viewing
        
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if 'lessons' in self.context['request'].path:
            fields.pop('date_viewing', None)
        return fields


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'owner',
            'lessons',
        )
