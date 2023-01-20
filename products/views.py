from django.shortcuts import render
from . models import Product, Category, Tag, Comment
from discussion.models import Comment as DiscussComment
from django.views.generic import DeleteView
from . forms import CommentForm
from django.http import HttpResponseRedirect
from pages.models import Profile
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from discussion.models import Discuss
from django.http import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View



def product_list(request):
    products =  Product.objects.all() # .order_by(date)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, "designs.html", context)

def product_detail(request, category_slug, product_id):
    current_user = request.user
    product = Product.objects.get(category__slug = category_slug, id = product_id)

    profile = product.seller
    products = Product.objects.filter(seller = profile)
    posts = Discuss.objects.filter(author = profile)
    comments_profile = DiscussComment.objects.filter(user = profile)
    product_comments_profile = Comment.objects.filter(user = profile)

    total_like_of_profile = 0
    for product_like in products:
        total_like_of_profile += len(product_like.get_likes)    
    for post_like in posts:
        total_like_of_profile += len(post_like.get_likes)
    for comment_like in comments_profile:
        total_like_of_profile += len(comment_like.get_likes)
    for comment_dislike in comments_profile:
        total_like_of_profile -= len(comment_dislike.get_dislikes)
    for comment_like in product_comments_profile:
        total_like_of_profile += len(comment_like.get_likes)
    for comment_dislike in product_comments_profile:
        total_like_of_profile -= len(comment_dislike.get_dislikes) 

    total_products = Product.objects.filter(seller = profile).count()

    tags = Tag.objects.all()

    comments = Comment.objects.filter(product=product) # comment starts
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = Profile.objects.get(id = current_user.id)
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm() # comment ends


    total_like = product.likes.all().count()
    if current_user.is_authenticated:
        fav_product = current_user.favorite_products.all()
        like_product = current_user.liked_products.all()
    else:
        fav_product = None
        like_product = None

    context = {
        'product': product,
        'products': products[:8],
        'profile': profile,
        'tags': tags,
        'fav_product': fav_product,
        'like_product': like_product,
        'comment_form': form,
        'comments': comments,
        'total_like': total_like,
        'total_products': total_products,
        'total_like_of_profile': total_like_of_profile,
        }
    return render(request, 'product.html', context)

def order_by_products(request):
    products =  Product.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.GET.get('Newest to Oldest') == 'Newest to Oldest':
        products = products.order_by('date')
    if request.GET.get('Oldest to Newest') == 'Oldest to Newest':
        products = products.order_by('-date')
    if request.GET.get('Highest to Lowest') == 'Highest to Lowest':
        products = products.order_by('-price')
    if request.GET.get('Lowest to Highest') == 'Lowest to Highest':
        products = products.order_by('price')
    if request.GET.get('Most Liked') == 'Most Liked':
        products = Product.objects.annotate(l_count = Count('likes')).order_by('-l_count')
    if request.GET.get('prc0to30') == '0-30 TL arası':
        products = Product.objects.filter(price__gt = 0, price__lte = 10)


    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, "designs.html", context)

def delete_comment(request):
    if request.method == "POST":
        category_slug = request.POST["category_slug"]
        product_id = request.POST["product_id"]
        product = Product.objects.get(category__slug = category_slug, id = product_id)
        comments = Comment.objects.filter(product=product)
        comment = comments.get(id = request.POST["comment_id"])
        comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def category_list(request, category_slug):
    products = Product.objects.filter(category__slug = category_slug)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, 'designs.html', context)

def tag_list(request, tag_slug):
    products = Product.objects.all().filter(tags__slug = tag_slug)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, 'designs.html', context)

@login_required(login_url = "login")
def favorite_list(request):
    current_user = request.user
    products = current_user.favorite_products.all().order_by('date')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, 'designs.html', context)

@login_required(login_url = "login")
def liked_list(request):
    current_user = request.user
    products = current_user.liked_products.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, 'designs.html', context)

def search(request):
    searchedfor = request.GET['search']
    products = Product.objects.filter(name__contains = searchedfor)
    categories = Category.objects.all()
    tags= Tag.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'tags':tags,
        'searchedfor': searchedfor,
    }

    return render(request, 'designs.html', context)

class ProductCommentReplyView(LoginRequiredMixin, View):
    def post(self, request, category_slug, product_pk, pk, *args, **kwargs):
        product = Product.objects.get(category__slug = category_slug, pk = product_pk)
        parent_comment = Comment.objects.get(pk = pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = Profile.objects.get(id = request.user.id)
            new_comment.product = product
            new_comment.parent = parent_comment
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AddProductCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddProductCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
# Create your views here.
