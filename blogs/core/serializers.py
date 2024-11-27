from rest_framework import serializers
from .models import Post,Tag,Menu,Rating,Reaction,Comment
from auth_app.serializers import UserSerializer




class SimpleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','name']


class MenuSerializer(serializers.ModelSerializer):
    # parent = serializers.StringRelatedField()
    class Meta:
        model = Menu
        fields = ['id','name','slug','parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name','fa_name']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','post','user','rate']
        read_only_fields=['id','user']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id','user','comment','reaction_type']
        read_only_fields = ['id','user']
        # extra_kwargs={'comment':{'write_only':True}}

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)
        

class PostSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    menu = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True,read_only=True)
    seos = serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ['id','title','slug','menu','image','author','rate','description','content','read_time','seos','tags','created_on','updated_on','status']
        read_only_fields = ['id','rate','created_on','updated_on','status']


    def get_rate(self,instance):
        return instance.avg_rate
    
    
class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','user','text','post']
        read_only_fields = ['id','user']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)




class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    class Meta(SimpleCommentSerializer.Meta):
        model = Comment
        fields = ['id','user','text','post','likes','dislikes']
        read_only_fields = ['id','user','text','post','likes','dislikes']

    def get_likes(self,instance):
        return instance.likes
    def get_dislikes(self,instance):
        return instance.dislikes