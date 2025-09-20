from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todolist.views import TodoViewSet

#τα imports του spectacular
from drf_spectacular.views import SpectacularAPIView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    #spectacular νεα paths
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),   #το json file
]
