from django.urls import path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserRegister.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
]

router = routers.SimpleRouter()
router.register('', views.UserViewSet)
urlpatterns += router.urls
