from rest_framework import serializers
from .models import Post,Tag,Menu,Rating,Reaction





class SimpleCategorySerializer(serializers.ModelSerializer):
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
        fields = ['id','value']


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
        fields = ['id','user','post','reaction_type']
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
    # images = ProductImageSerializer(read_only=True,many=True)

    class Meta:
        model = Post
        fields = ['id','title','slug','menu','image','author','content','tags','created_on','updated_on','status']
        read_only_fields = ['id','rate','created_on','updated_on']


    def get_rate(self,instance):
        return instance.avg_rate
    