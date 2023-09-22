import django_filters
from django.shortcuts import get_object_or_404

from .models import Product, UserProduct


class LessonFilter(django_filters.FilterSet):

    in_product = django_filters.NumberFilter(
        field_name='tags__slug',
        method='in_product_filter'
    )

    def in_product_filter(self, queryset, name, value):
        product = get_object_or_404(Product, id=value)
        user = self.request.user
        if UserProduct.objects.filter(product=product, user=user).exists():
            lessons_in_product = product.lessons.all()
            return queryset.filter(
                id__in=lessons_in_product.values_list('lesson_product',)
            )
        return queryset.none()
