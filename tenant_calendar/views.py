from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


from .models import (
    User, ConferenceRoom, Calendar
)
from .serializers import (
    CalendarSerializer, ConferenceRoomSerializer, UserSerializer)


class CompanyAPIMixin(mixins.CreateModelMixin):
    # This could also be implemented with permissions

    def create(self, request, *args, **kwargs):
        data = request.data
        if request.user.is_superuser:
            data['user'] = request.data.get('user')
        else:
            data['user'] = request.user.pk

        data['company_i'] = request.user.company_i.pk

        # Help build nested data
        location = request.data.get('location', None)
        if location:
            location['company_i'] = request.user.company_i.pk

        # Serialize data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class CalendarAPIView(
        CompanyAPIMixin, generics.CreateAPIView, generics.ListAPIView):
    serializer_class = CalendarSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['event_name', 'meeting_agenda']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            calendar = Calendar.objects.filter(
                company_i=self.request.user.company_i)
            # Get queryset of user event as participant
            qs_1 = calendar.filter(
                participants__id=self.request.user.id)
            # Get queryset of user event as host
            qs_2 = calendar.filter(user=self.request.user)
            # merge the querysets
            calendar = qs_1 | qs_2
        else:
            calendar = Calendar.objects.all()
        conf_room = self.request.query_params.get('location_id')
        day = self.request.query_params.get('day')
        if day:
            calendar = calendar.filter(start_time__date=day)
        if conf_room:
            calendar = calendar.filter(location__name=conf_room)

        return calendar


class ConferenceRoomAPIView(CompanyAPIMixin,
                            generics.CreateAPIView, generics.ListAPIView):
    serializer_class = ConferenceRoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            conference_room = ConferenceRoom.objects.filter(
                company_i=self.request.user.company_i)
        else:
            conference_room = ConferenceRoom.objects.all()

        return conference_room


class UserAPIView(CompanyAPIMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
