from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.conf import settings




class Menu(models.Model):
    name = models.CharField(max_length=50,unique=True)
    fa_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='childs')

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['slug','parent'],name='unique_slug_category')
        ]

    def __str__(self) -> str:
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=30,unique=True)
    fa_name = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.value
    
class Seo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    canonical = models.CharField(max_length=100)
    
# chand ta text - video?
# class Description(models.Model):
#     video = models.FileField(upload_to='video')
#     text = models.TextField()


class Post(models.Model):
    STATUS_CHOICES = (
        ('D','Draft'),
        ('P','Publish')
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='D')
    menu = models.ForeignKey(Menu,on_delete=models.PROTECT,related_name='posts')
    tags = models.ManyToManyField(Tag,blank=True,related_name='posts')
    seos = models.ManyToManyField(Seo,blank=True,related_name='posts')

    def __str__(self):
        return self.title





class Rating(models.Model):
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='rates')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user','post'),name='unique_rate')
        ]


class Reaction(models.Model):
    REACTION_OPTIONS = (('L','Like'),('D','Dislike'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='reactions')
    reaction_type = models.CharField(max_length=1,choices=REACTION_OPTIONS)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user','post'),name='unique_reaction')
        ]


