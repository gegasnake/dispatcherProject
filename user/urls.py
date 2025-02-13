from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import RegisterView, UserProfileView, PasswordChangeView, UserStatisticsView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/change-password/", PasswordChangeView.as_view(), name="change-password"),
    path("profile/statistics/", UserStatisticsView.as_view(), name="user-statistics"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
]
