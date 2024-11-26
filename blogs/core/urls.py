from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView\
                                ,SpectacularSwaggerView

from .views import MenuViewSet,BlogViewSet,TagViewSet





router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'tag', TagViewSet)






urlpatterns = [
    # path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
    
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   
]