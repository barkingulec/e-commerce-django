from django.db import models
from pages.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, null = True)
    slug = models.SlugField(max_length=50, unique = True, null = True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, null = True)
    slug = models.SlugField(max_length=50, unique = True, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, unique = True)
    category = models.ForeignKey(Category, null = True, on_delete = models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank = True)
    favorites = models.ManyToManyField(User, blank = True, related_name="favorite_products")
    likes = models.ManyToManyField(User, blank = True, related_name="liked_products")
    description = models.TextField(blank = True, null = True)
    image = models.ImageField(upload_to ="products/%Y/%m/%d", default = "images/default.png")
    date = models.DateTimeField(auto_now = True)
    available = models.BooleanField(default = True)
    price = models.DecimalField(default = 0 ,max_digits = 6, decimal_places = 2)

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
        return reverse('product_detail', args=(str(self.category).lower(), str(self.id)))

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="comment", on_delete = models.CASCADE)
    user = models.ForeignKey(Profile, null = True, on_delete = models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, blank=True, related_name='product_comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='product_comment_dislikes')
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
        return '%s - %s' % (self.product.name, self.user)

# Create your models here.
