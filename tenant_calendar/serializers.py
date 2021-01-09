from rest_framework import serializers

from .models import (
    User, ConferenceRoom, Calendar, Company
)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name',)


class CompanySerializerMixin(metaclass=serializers.SerializerMetaclass):
    company_i = CompanySerializer(read_only=True)


class ConferenceRoomSerializer(CompanySerializerMixin,
                               serializers.ModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = '__all__'


class UserSerializer(CompanySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'full_name', 'company_id',
                  'default_timezone', 'company_i')


class CalendarSerializer(CompanySerializerMixin, serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    participants = serializers.ListField(
        source='user.email', child=serializers.EmailField())
    location = ConferenceRoomSerializer(read_only=True)

    class Meta:
        model = Calendar
        fields = '__all__'
