# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from api.models import Race, Sex, MoneyType, Attribute, Arsenal, Action, UserArsenal, Experience, \
    Transaction, Location, UserLocation, ExperienceCount, Mob, MobArsenal


class RaceAdmin(admin.ModelAdmin):
    pass


class SexAdmin(admin.ModelAdmin):
    pass


class MoneyTypeAdmin(admin.ModelAdmin):
    pass


class AttributeInline(admin.TabularInline):
    model = Attribute


class ArsenalAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInline,
    ]
    filter_horizontal = ('location',)


class ActionAdmin(admin.ModelAdmin):
    pass


class UserArsenalAdmin(admin.ModelAdmin):
    pass


class ExperienceAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    filter_horizontal = ('passages',)


class UserLocationAdmin(admin.ModelAdmin):
    pass


class ExperienceCountAdmin(admin.ModelAdmin):
    pass


class MobAdmin(admin.ModelAdmin):
    filter_horizontal = ('locations',)


class MobArsenalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Race, RaceAdmin)
admin.site.register(Sex, SexAdmin)
admin.site.register(MoneyType, MoneyTypeAdmin)
admin.site.register(Arsenal, ArsenalAdmin)
admin.site.register(UserArsenal, UserArsenalAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(ExperienceCount, ExperienceCountAdmin)
admin.site.register(Mob, MobAdmin)
admin.site.register(MobArsenal, MobArsenalAdmin)
