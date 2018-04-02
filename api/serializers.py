from rest_framework import serializers
from api.models import User, Arsenal, Location


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'race', 'sex', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArsenalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arsenal
        fields = ('id', 'type', 'name', 'strength', 'level', 'money_type', 'cost', 'location')


class LocationSerialize(serializers.ModelSerializer):
    arsenals = ArsenalSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'level', 'passages', 'name', 'arsenals')


