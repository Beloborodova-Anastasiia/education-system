import datetime

from django.contrib.auth import get_user_model
from django.db import models

from .const import PASSING_THRESHOLD, STATUS_NOT_VIEWD, STATUS_VIEWED

User = get_user_model()


class Lesson(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
        verbose_name='Название',
    )
    link = models.URLField(
        unique=True,
        verbose_name='Ссылка на урок',
        blank=True,
        null=True
    )
    duration = models.IntegerField(
        verbose_name='Длительность урока ',
        default=0
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField(
        max_length=256,
        db_index=True,
        verbose_name='Название',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец',
    )
    lessons = models.ManyToManyField(
        Lesson,
        through='LessonProduct',
        verbose_name='Уроки',
    )
    users = models.ManyToManyField(
        User,
        through='UserProduct',
        verbose_name='Пользователи',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class LessonProduct(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_product',
        verbose_name='Урок',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='lesson_product',
        verbose_name='Продукт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lesson', 'product'],
                name='unique_lesson_product',
            )
        ]
        verbose_name_plural = 'Уроки в составе продукта'
        verbose_name = 'Уроки'


class UserProduct(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_user',
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product',
            )
        ]
        verbose_name_plural = 'Продукты пользователя'
        verbose_name = 'Продукты'

    def save(self, *args, **kwargs):
        if self.pk is None:
            lessons = self.product.lessons.all()
            print(lessons)
            for lesson in lessons:
                print(lesson)
                UserLesson.objects.get_or_create(user=self.user, lesson=lesson)
        super().save(*args, **kwargs)


class UserLesson(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_user',
        verbose_name='Пользователь',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_user',
        verbose_name='Урок',
    )
    status = models.TextField(
        max_length=15,
        verbose_name=' Статус',
    )
    view_duration = models.IntegerField(
        verbose_name='Время просмотра',
        default=0
    )
    view_date = models.DateField(
        verbose_name='Дата просмотра',
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'lesson'],
                name='unique_user_lesson',
            )
        ]
        verbose_name_plural = 'Уроки пользователя'
        verbose_name = 'Уроки'

    def save(self, *args, **kwargs):
        if (
            self.viewing_duration / self.lesson.duration
            >= PASSING_THRESHOLD
        ):
            self.status = STATUS_VIEWED
        else:
            self.status = STATUS_NOT_VIEWD
        if self.viewing_duration > 0:
            self.date_viewing = str(datetime.date.today())
        super(UserLesson, self).save(*args, **kwargs)
