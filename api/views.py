# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated

from api.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(methods=['get'])
    def get_stats(self, request, pk=None):
        user = User.objects.get(id=pk)
        if user:
            return Response(user.get_stats())
