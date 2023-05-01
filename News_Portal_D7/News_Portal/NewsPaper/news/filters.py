import placeholder as placeholder
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from django import forms

from .models import Post, Author


# Создаем свой набор фильтров для модели.
# FilterSet, который мы наследуем, должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    heading = CharFilter(field_name='heading', lookup_expr='icontains', label='Название')
    author = ModelChoiceFilter(field_name='author', lookup_expr='exact', queryset=Author.objects.all(), label='Автор',
                               empty_label='любой')
    date = DateFilter(field_name='datetime', widget=forms.DateInput(attrs={'type': 'date'}), label='Позже',
                      lookup_expr='date__gte')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            #'heading': ['icontains'],
            #'author': ['exact'],
            #'author__user__username': ['exact'],
            #'author': ['in'],
            # количество товаров должно быть больше или равно
            #'datetime': ['gt'],
        }