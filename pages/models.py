from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    username = models.CharField(null = True, max_length=50)
    pw = models.CharField(null = True, max_length=50)
    first_name = models.CharField(null = True, blank = True, max_length = 100)
    last_name = models.CharField(null = True, blank = True, max_length = 100)
    description = models.TextField(blank=True)
    image = models.ImageField(default="images/default.png",upload_to="profiles/%Y/%m/%d/")
    thumbnail = models.ImageField(default="/images/thumbnail.png",upload_to="profiles/%Y/%m/%d/")
    facebook = models.URLField(max_length=100, null = True, blank=True)
    twitter = models.URLField(max_length=100, null = True, blank=True)
    instagram = models.URLField(max_length=100, null = True, blank=True)
    youtube = models.URLField(max_length=100, null = True, blank=True)
    is_seller = models.BooleanField(default = False)
    followers = models.ManyToManyField("Follow")

    def __str__(self):
        return str(self.username)

class Contact(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    message = models.TextField()

    def __str__(self):
        return self.email

class Follow(models.Model):
    followed = models.ForeignKey(
        Profile,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    followed_by = models.ForeignKey(
        Profile,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.followed_by.username} started following {self.followed.username}"
# Create your models here.
