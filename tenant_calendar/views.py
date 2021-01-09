from rest_framework import status, generics, mixins
from rest_framework.response import Response
from django.utils.timezone import timezone, timedelta

from .models import (
    User, ConferenceRoom, Calendar
)
from .serializers import (
    CalendarSerializer, ConferenceRoomSerializer, UserSerializer)


class CompanyAPIMixin(mixins.CreateModelMixin, mixins.ListModelMixin):
    # This could also be implemented with permissions

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.data.get('user', request.user.pk)

        data['company_i'] = request.user.company_i.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        # Restrict queryset available in user's company
        if not request.user.is_superuser:
            qs = self.get_queryset().filter(company_i=request.user.company_i)
        else:
            qs = self.get_queryset()

        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class CalendarAPIView(CompanyAPIMixin,
                      generics.CreateAPIView, generics.ListAPIView):
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()

    # def post(self, *args, **kwargs):
    #     user = self.request.user
    #     print(user.username)
    #     data = self.request.data
    #     data['user'] = user.pk
    #     print(data)

    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({'message': 'Event created'},
    #                     status=status.HTTP_201_CREATED)


class ConferenceRoomAPIView(CompanyAPIMixin,
                            generics.CreateAPIView, generics.ListAPIView):
    serializer_class = ConferenceRoomSerializer
    queryset = ConferenceRoom.objects.all()


class UserAPIView(CompanyAPIMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
