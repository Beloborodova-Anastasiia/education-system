from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers

from .const import PATH_TO_LESSONS, STATUS_VIEWED
from .models import Lesson, Product, UserLesson, UserProduct

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    view_duration = serializers.SerializerMethodField()
    view_date = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'link',
            'duration',
            'status',
            'view_duration',
            'view_date'
        )

    def get_status(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().status
        return None

    def get_view_duration(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().view_duration
        return None

    def get_view_date(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().view_date
        return None

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if self.context['request'].path == PATH_TO_LESSONS:
            fields.pop('view_date', None)
        return fields


class StatisticsSerializer(serializers.ModelSerializer):
    lessons_viewed = serializers.SerializerMethodField()
    view_time = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    acquisition_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'lessons_viewed',
            'view_time',
            'users_count',
            'acquisition_percentage'
        )

    def get_lessons_viewed(self, obj):
        users_lessons = UserLesson.objects.filter(status=STATUS_VIEWED)
        return obj.lessons.filter(
            id__in=users_lessons.values_list('lesson',)
        ).all().count()

    def get_view_time(self, obj):
        lessons = obj.lessons.all()
        return UserLesson.objects.filter(
            id__in=lessons.values_list('lesson_user',)
        ).aggregate(Sum('view_duration'))['view_duration__sum']

    def get_users_count(self, obj):
        return UserProduct.objects.filter(
            product=obj
        ).count()

    def get_acquisition_percentage(self, obj):
        count_users_all = User.objects.all().count()
        users_count = UserProduct.objects.filter(
            product=obj
        ).count()
        return users_count / count_users_all * 100
