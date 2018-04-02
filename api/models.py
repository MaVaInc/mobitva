# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CustomUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        user = self.model(
            username=kwargs['username'],
            race=Race.objects.get(id=kwargs['race']),
            sex=Sex.objects.get(id=kwargs['sex'])
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
        return self.arsenals.filter(dressed=True).values(name=F('arsenal__stats__type__name')) \
            .annotate(attributes=Sum('arsenal__stats__stat'))

    def get_balance(self):
        return self.balance.select_related('type').values(name=F('type__name')).annotate(value=Sum('value'))

    def get_current_location(self):
        return self.pathways.select_related('location').values(name=F('location__name'), pk=F('location__id')).last()

    def get_level(self):
        user_exp = self.experiences.aggregate(value=Sum('count')).get('value')
        return ExperienceCount.objects.filter(
            count__gte=user_exp).values('level').annotate(percent=(user_exp * 100) / F('count')).order_by('level').first()


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
    money_type = models.ForeignKey('MoneyType', on_delete=models.DO_NOTHING, )
    cost = models.IntegerField()
    location = models.ManyToManyField('Location', related_name='items')

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    type = models.ForeignKey('Action', on_delete=models.CASCADE, related_name='attributes')
    stat = models.IntegerField()
    arsenal = models.ForeignKey('Arsenal', on_delete=models.CASCADE, related_name='stats')


class UserArsenal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='arsenals')
    arsenal = models.ForeignKey('Arsenal', on_delete=models.CASCADE, related_name='users')
    dressed = models.BooleanField(default=False)
    strength = models.IntegerField()

    def __str__(self):
        return self.user.username + '|' + self.arsenal.name


class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='experiences')
    count = models.IntegerField()

    def __str__(self):
        return self.user.username + '|' + str(self.count)


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='balance')
    value = models.IntegerField()
    type = models.ForeignKey('MoneyType', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username + '|' + str(self.value)


class Location(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    passages = models.ManyToManyField('Location')

    def __str__(self):
        return self.name


class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pathways')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='travelers')


class ExperienceCount(models.Model):
    level = models.IntegerField()
    count = models.IntegerField()

    def __str__(self):
        return str(self.level)


class Mob(models.Model):
    name = models.CharField(max_length=50)
    locations = models.ManyToManyField('Location', related_name='mobs')

    def __str__(self):
        return self.name


class MobArsenal(models.Model):
    mob = models.ForeignKey('Mob', on_delete=models.CASCADE, related_name='arsenals')
    arsenal = models.ForeignKey('Arsenal', on_delete=models.CASCADE, related_name='mobs')
    dressed = models.BooleanField(default=False)

    def __str__(self):
        return self.mob.name + '| ' + self.arsenal.name


class Arena(models.Model):
    TYPE_CHOICES = (
        ('wall_to_wall', 'Стенка на стенку'),
        ('survival', 'Выживание'),
        ('open_fight', 'Открытый бой'),
        ('mob_fight', 'Бой с мобом'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)


class ArenaMembers(models.Model):
    SIDE_CHOICES = (
        ('left', 'Левая'),
        ('right', 'Правая'),
    )
    side = models.CharField(max_length=20, choices=SIDE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    arena = models.ForeignKey('Arena', on_delete=models.CASCADE, related_name='members')