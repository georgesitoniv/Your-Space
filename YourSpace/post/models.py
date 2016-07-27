from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
 

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField(max_length=600, blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_post", symmetrical=False)
    total_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return "Post by {}".format(self.user.username)

    def has_liked(self, user):
               
        if self.likes.filter(id=user.id).exists():
            liked = True
        else:
            liked = False
        
        return liked

class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null= True)
    content = models.TextField(max_length=400, blank=True)

   