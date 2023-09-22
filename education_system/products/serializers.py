from django.db.models import Sum
from rest_framework import serializers

from .models import Lesson, Product, User, UserLesson, UserProduct


class LessonSerializer(serializers.ModelSerializer):
    PATH_TO_LESSONS = '/api/lessons/'
    status = serializers.SerializerMethodField()
    viewing_duration = serializers.SerializerMethodField()
    date_viewing = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'link',
            'duration',
            'status',
            'viewing_duration',
            'date_viewing'
        )

    def get_status(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().status
        return None

    def get_viewing_duration(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().viewing_duration
        return None

    def get_date_viewing(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(lesson=obj, user=user)
        if user_lesson.exists():
            return user_lesson.first().date_viewing
        return None

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if self.context['request'].path == self.PATH_TO_LESSONS:
            fields.pop('date_viewing', None)
        return fields


class StatisticsSerializer(serializers.ModelSerializer):
    VIEWED_STATUS = 'Просмотрено'

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
        users_lessons = UserLesson.objects.filter(status=self.VIEWED_STATUS)
        return obj.lessons.filter(
            id__in=users_lessons.values_list('lesson',)
        ).all().count()

    def get_view_time(self, obj):
        lessons = obj.lessons.all()
        return UserLesson.objects.filter(
            id__in=lessons.values_list('lesson_user',)
        ).aggregate(Sum('viewing_duration'))['viewing_duration__sum']

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
