from rest_framework_simplejwt import views as jwt_views
from . import views
from django.urls import path, include
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',signup),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('change/', ChangePasswordView.as_view(), name='change-password'),
    # path('profile/',views.ProfileDispatcher.as_view(),name="profile_dispathcher"),
    path('profile/', ProfileView.as_view()),
    path('profile/create/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('getme/',getme),
]