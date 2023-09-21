# from django.shortcuts import get_object_or_404
# from django.utils.datastructures import MultiValueDictKeyError

from django.db.models import Sum
from rest_framework import serializers

from .models import (Lesson, Product, User,
                     UserProduct, UserLesson)


class LessonSerializer(serializers.ModelSerializer):
    USER_LESSON = None

    status = serializers.SerializerMethodField()
    viewing_duration = serializers.SerializerMethodField()
    date_viewing = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'name',
            'link',
            'duration',
            'status',
            'viewing_duration',
            'date_viewing'
        )

    def get_status(self, obj):
        if self.USER_LESSON is not None:
            if self.USER_LESSON.exists():
                return self.USER_LESSON.first().status
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        self.USER_LESSON = user_lesson
        if user_lesson.exists():
            return user_lesson.first().status

    def get_viewing_duration(self, obj):
        if self.USER_LESSON is not None:
            if self.USER_LESSON.exists():
                return self.USER_LESSON.first().viewing_duration
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        self.USER_LESSON = user_lesson
        if user_lesson.exists():
            return user_lesson.first().viewing_duration

    def get_date_viewing(self, obj):
        if self.USER_LESSON is not None:
            if self.USER_LESSON.exists():
                return self.USER_LESSON.first().date_viewing
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        self.USER_LESSON = user_lesson
        if user_lesson.exists():
            return user_lesson.first().date_viewing

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        print(self.context['request'].path)
        if self.context['request'].path == '/api/products/':
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


class StatisticsSerializer(serializers.ModelSerializer):
    lessons_viewed = serializers.SerializerMethodField()
    view_time = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    acquisition_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'lessons_viewed',
            'view_time',
            'users_count',
            'acquisition_percentage'
        )

    def get_lessons_viewed(self, obj):
        users_lessons = UserLesson.objects.filter(status='Просмотрено')
        lessons_viewed = obj.lessons.filter(
            id__in=users_lessons.values_list('lesson',)
        ).all().count()
        return lessons_viewed

    def get_view_time(self, obj):
        lessons = obj.lessons.all()
        time_view = UserLesson.objects.filter(
            id__in=lessons.values_list('userlesson',)
        ).aggregate(Sum('viewing_duration'))['viewing_duration__sum']
        return time_view

    def get_users_count(self, obj):
        users_count = UserProduct.objects.filter(
            product=obj
        ).count()
        return users_count

    def get_acquisition_percentage(self, obj):
        count_users_all = User.objects.all().count()
        users_count = UserProduct.objects.filter(
            product=obj
        ).count()
        percentage = users_count / count_users_all * 100
        return percentage
