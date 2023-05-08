from rest_framework_simplejwt import views as jwt_views
from .views import *
from django.urls import path



app_name = 'accounts'
urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',signup),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('change/', ChangePasswordView.as_view(), name='change-password'),


]