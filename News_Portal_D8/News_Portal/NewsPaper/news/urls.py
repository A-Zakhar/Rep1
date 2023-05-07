from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    #В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,а Django ожидает функцию, нам надо представить этот класс в виде view.
    path('', PostsList.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
