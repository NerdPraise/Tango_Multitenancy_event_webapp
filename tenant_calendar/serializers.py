from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from datetime import timedelta

from .models import (
    User, ConferenceRoom, Calendar, Company
)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name',)


class CompanySerializerMixin(metaclass=serializers.SerializerMetaclass):
    company_i = CompanySerializer(required=True)


class ConferenceRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        company_i = representation['company_i']
        representation['company_i'] = Company.objects.get(pk=company_i).name
        return representation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'full_name', 'company_id',
                  'default_timezone', 'company_i')


class CalendarSerializer(serializers.ModelSerializer):
    participants = serializers.ListField(write_only=True)
    location = ConferenceRoomSerializer(required=False)
    end_time = serializers.DateTimeField()
    start_time = serializers.DateTimeField()

    class Meta:
        model = Calendar
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        company_i = representation['company_i']
        representation['company_i'] = Company.objects.get(pk=company_i).name

        if instance.participants:
            representation['participants'] = [
                user.email for user in instance.participants.all()]
        # if instance.location:
        #     location_id = representation['location']['id']
        #     representation['location'] = ConferenceRoom.objects.get(
        #         pk=location_id).name
        return representation

    def validate_participants(self, data):
        new_data = []
        for value in data:
            try:
                user = User.objects.get(email=value)
                new_data.append(user)
            except User.DoesNotExist:
                raise ValidationError({f'{value}': 'No user with this email'})

        return new_data

    def validate(self, data):
        super().validate(data)
        end_time = data['end_time']
        start_time = data['start_time']
        max_end_time = start_time + timedelta(hours=8)
        if start_time >= end_time:
            raise ValidationError(
                {'end_time': 'End time must occur after start time'})
        if end_time > max_end_time:
            raise serializers.ValidationError(
                {'end_time': 'You can\'t schedule an event for more than 8 hours'})
        return data

    def create(self, validated_data):
        location = validated_data.pop('location', None)
        participants = validated_data.pop('participants')
        calendar = Calendar.objects.create(**validated_data)

        if location:
            try:
                conference = ConferenceRoom.objects.get(
                    name=location['name'], company_i=calendar.company_i)
            except ConferenceRoom.DoesNotExist:
                raise ValidationError(
                    {'location': 'This room doesn\'t exist in this company'})

            calendar.location = conference
            calendar.save()
        return calendar
