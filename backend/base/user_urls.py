from django.urls import path
from . import user_views as views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('reset/', views.resetUserPassword, name='reset-password'),
    # path('new/', views.setNewPassword, name='set-password'),
    path('logout/', views.logout, name='logout'),
    # Add logout
]