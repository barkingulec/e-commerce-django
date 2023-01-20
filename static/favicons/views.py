from django.shortcuts import render
from . models import Product, Category, Tag, Comment
from django.views.generic import DeleteView
from . forms import CommentForm
from django.http import HttpResponseRedirect


def product_list(request):
    products =  Product.objects.all() # .order_by(date)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    date_new_to_old = products.order_by('date').values()
    date_old_to_new = products.order_by('-date')
    price_high_to_low = products.order_by('price')
    price_low_to_high = products.order_by('-price')

    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        'date_new_to_old': date_new_to_old,
        'date_old_to_new': date_old_to_new,
        'price_high_to_low': price_high_to_low,
        'price_low_to_high': price_low_to_high,
        }
    return render(request, "designs.html", context)

def product_detail(request, category_slug, product_id):
    current_user = request.user
    product = Product.objects.get(category__slug = category_slug, id = product_id)

    profile = product.seller
    products = Product.objects.filter(seller = profile)

    total_like_of_profile = 0
    for product_like in products:
        total_like_of_profile += len(product_like.get_likes)    

    total_products = Product.objects.filter(seller = profile).count()

    tags = Tag.objects.all()

    comments = Comment.objects.filter(product=product) # comment starts

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = current_user
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

def category_list(request, category_slug):
    products = Product.objects.all().filter(category__slug = category_slug)
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

def search(request):
    products = Product.objects.filter(name__contains = request.GET['search'])
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        }
    return render(request, 'designs.html', context)

# Create your views here.
