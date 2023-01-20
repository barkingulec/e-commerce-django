from django.db import models
from pages.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from django.utils.text import slugify

class Discuss(models.Model):
    author = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, unique = True)
    #category = models.ForeignKey(Category, null = True, on_delete = models.DO_NOTHING)
    favorites = models.ManyToManyField(User, blank = True, related_name="favorite_discuss")
    likes = models.ManyToManyField(User, blank = True, related_name="liked_discuss")
    description = models.TextField(blank = True, null = True)
    image = models.ImageField(upload_to ="discuss/%Y/%m/%d", default = "images/default.png", blank = True, null = True)
    date = models.DateTimeField(auto_now = True)

    @property
    def get_likes(self):
        likes = self.likes.all()
        likes_list = []
        for like in likes:
            likes_list.append(like.username)

        return likes_list

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id), str(self.name)))

class Comment(models.Model):
    post = models.ForeignKey(Discuss, related_name="post_comment", on_delete = models.CASCADE)
    user = models.ForeignKey(Profile, related_name="comment_user", null = True, on_delete = models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE, related_name = "+")

    @property
    def get_likes(self):
        likes = self.likes.all()
        likes_list = []
        for like in likes:
            likes_list.append(like.username)

        return likes_list
    
    @property
    def get_dislikes(self):
        dislikes = self.dislikes.all()
        dislikes_list = []
        for dislike in dislikes:
            dislikes_list.append(dislike.username)

        return dislikes_list

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by("-date_added").all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return '%s - %s' % (self.post.name, self.user)
    

# Create your models here.
