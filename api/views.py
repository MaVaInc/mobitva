# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from api.models import User, Arsenal, Location
from api.serializers import UserSerializer, ArsenalSerializer, LocationSerialize
from api.permissions import IsAdminOrSelf


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    @detail_route(methods=['get'])
    def get_stats(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        self.check_object_permissions(self.request, user)
        return Response({'success': True, 'data': user.get_stats()})

    @detail_route(methods=['get'])
    def balance(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        self.check_object_permissions(self.request, user)
        return Response({'success': True, 'data': user.get_balance()})

    @detail_route(methods=['get'])
    def get_current_location(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        self.check_object_permissions(self.request, user)
        return Response({'success': True, 'data': user.get_current_location()})

    @detail_route(methods=['get'])
    def get_level(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        self.check_object_permissions(self.request, user)
        return Response({'success': True, 'data': user.get_level()})


class ArsenalViewSet(viewsets.ModelViewSet):
    serializer_class = ArsenalSerializer
    queryset = Arsenal.objects.prefetch_related('location').all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerialize
    queryset = Location.objects.prefetch_related('passages', 'items__location').all()

    def create(self, request, *args, **kwargs):
        self.permission_classes = (IsAdminUser,)
        return super(LocationViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.permission_classes = (IsAdminUser,)
        return super(LocationViewSet, self).update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.permission_classes = (IsAuthenticated,)
        return super(LocationViewSet, self).list(request, *args, **kwargs)


#hello