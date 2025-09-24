from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todolist.views import TodoViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
#τα imports του spectacular
from drf_spectacular.views import SpectacularAPIView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    #spectacular νεα paths
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),   #το json file

    #paths για tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   #εδώ είναι το login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
