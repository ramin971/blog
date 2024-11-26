from rest_framework import viewsets,mixins,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError

from .permissions import IsOwnerOrReadOnly
from .models import Menu,Post,Rating,Reaction,Tag
from .serializers import MenuSerializer,RatingSerializer,ReactionSerializer,TagSerializer,PostSerializer
from django.db.models import Avg



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RatingPost(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        return {'user':self.request.user}
    

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related('post__author','post','user').all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    

    def create(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        reaction_type = request.data.get('reaction_type')
        try:
            existing_reaction = Reaction.objects.get(post_id=post_id,user=request.user)
            if existing_reaction.reaction_type == reaction_type:
                # print('same........')
                raise ParseError(detail='you have already reacted with this type.')
            else:
                # print('change........')
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                serializer = ReactionSerializer(existing_reaction)
                return Response(serializer.data)
        except Reaction.DoesNotExist:
            # print('except........')
            return super().create(request, *args, **kwargs)
        
    def get_serializer_context(self):
        return {'user':self.request.user}
  
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author','menu').prefetch_related('tags')\
        .annotate(avg_rate=Avg('rates__rate'))
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]