from rest_framework_simplejwt import views as jwt_views
from .views import *
from django.urls import path

from django.urls import path, include
from rest_framework import routers
from .views import *
#
# router = routers.DefaultRouter()
# router.register(r'user-profiles', ProfileViewSet)

app_name = 'accounts'
urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',signup),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('change/', ChangePasswordView.as_view(), name='change-password'),
    # path('', include(router.urls)),
    path('profile/', ProfileView.as_view()),
    path('profile/create/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
]