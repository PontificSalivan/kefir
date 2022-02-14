from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    secret_word = models.CharField(max_length=200, verbose_name='Секретное слово')
    favorite_colour = models.CharField(max_length=200, verbose_name='Любимый цвет')
    favorite_food = models.CharField(max_length=200, verbose_name='Любимая еда')

    def __str__(self):
        return self.name
