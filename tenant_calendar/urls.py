from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from .views import (
    CalendarAPIView, UserAPIView
)

app_name = 'calendar'

urlpatterns = [
    path('calendar/', CalendarAPIView.as_view(), name='calendar'),
    path('user/', UserAPIView.as_view(), name='user-list'),


    path('auth/login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
