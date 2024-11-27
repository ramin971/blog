from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView\
                                ,SpectacularSwaggerView

from .views import MenuViewSet,PostViewSet,TagViewSet,CommentViewSet,ReactionViewSet\
            ,RatingPost





router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'tag', TagViewSet)
router.register(r'comment',CommentViewSet,basename='comment')
router.register(r'reaction',ReactionViewSet)
router.register(r'rating',RatingPost)
router.register(r'post',PostViewSet)





urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('',include(router.urls)),
    
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   
]