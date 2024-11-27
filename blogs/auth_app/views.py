from .serializers import TokenRefreshSerializer,UserCreateSerializer,UserUpdateSerializer\
                ,ChangePasswordSerializer,UserSerializer
from .models import User
from .permissions import CreateOrIsAdmin
from core.paginations import CustomPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status,mixins,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf import settings



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination
    permission_classes =[CreateOrIsAdmin]

    def get_serializer_class(self):
        if self.action in ['update','partial_update']:
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        else:
            return UserSerializer

    # create_user / set refresh_cookie / add access_response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(password=serializer.validated_data['password'],**serializer.data)
        refresh_token = RefreshToken.for_user(user)
        
        # result = {**serializer.data , **{'access':str(refresh_token.access_token)}}
        response = Response(serializer.data , status=status.HTTP_201_CREATED)
        response.set_cookie('refresh_token', refresh_token, max_age=settings.COOKIE_MAX_AGE, httponly=True, path='/api/auth/jwt/refresh')
        return response

    @action(detail=False , methods=['get','put','delete'],permission_classes=[IsAuthenticated])
    def me(self,request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            
            # print('########get mycookie:',request.COOKIES.get('my_cookie'))
            # print('##########get_cookie',request.COOKIES.get('refresh_token'))
            # print(type(request.COOKIES.get('refresh_token')))
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method in ['PUT','PATCH']:
            serializer = UserUpdateSerializer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)




class ChangePassword(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user':self.request.user}
    
    # Change Status_Code of ChangePassword from 201 to 205
    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        result.status_code = 205
        return result



class CustomTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            # cookie_max_age = 3600 * 24 * 1 # 1 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=settings.COOKIE_MAX_AGE, httponly=True, path='/api/auth/jwt/refresh')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    # If SimpleJWT ROTATE_REFRESH_TOKENS = True :
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            # cookie_max_age = 3600 * 24 * 1 # 1 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=settings.COOKIE_MAX_AGE, httponly=True, path='/api/auth/jwt/refresh')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)