# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):

    def create_user(self, *args, **kwargs):
        user = self.model(
            race=kwargs['race'],
            sex=kwargs['sex']
        )
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.model(
            race=Race.objects.get(id=kwargs['race']),
            sex=Sex.objects.get(id=kwargs['sex']),
            username=kwargs['username']
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user


class User(AbstractUser):
    race = models.ForeignKey('Race', on_delete=models.CASCADE, related_name='populations')
    sex = models.ForeignKey('Sex', on_delete=models.CASCADE, related_name='members')
    object = CustomUserManager()

    REQUIRED_FIELDS = ['race', 'sex']
    USERNAME_FIELD = 'username'

    def get_stats(self):
        json = {
        }
        for user_stat in self.arsenals.filter(dressed=True).values('arsenal__stats__type__name').annotate(attributes=Sum('arsenal__stats__stat')):
            json[user_stat.get('arsenal__stats__type__name')] = user_stat.get('attributes')
        return json


class Race(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')

    def __str__(self):
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')

    def __str__(self):
        return self.name


class MoneyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Arsenal(models.Model):
    TYPE_CHOICES = (
        ('sword', 'Меч'),
        ('shield', 'Щит'),
        ('head', 'Голова'),
        ('hand', 'Рука'),
        ('body', 'Тело'),
        ('foot', 'Нога'),
        ('neck', 'Шея'),
        ('fingers', 'Пальцы')
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    strength = models.IntegerField()
    level = models.IntegerField()
    money_type = models.ForeignKey('MoneyType', on_delete=models.DO_NOTHING,)
    cost = models.IntegerField()

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    type = models.ForeignKey('Action', on_delete=models.DO_NOTHING, related_name='attributes')
    stat = models.IntegerField()
    arsenal = models.ForeignKey('Arsenal', on_delete=models.DO_NOTHING, related_name='stats')


class UserArsenal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='arsenals')
    arsenal = models.ForeignKey('Arsenal', on_delete=models.DO_NOTHING, related_name='users')
    dressed = models.BooleanField(default=False)
    strength = models.IntegerField()

    def __str__(self):
        return self.user.username + '|' + self.arsenal.name


class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,  related_name='experiences')
    count = models.IntegerField()

    def __str__(self):
        return self.user.username + '|' + self.count


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,related_name='balance')
    value = models.IntegerField()

    def __str__(self):
        return self.user.username + '|' + self.value
