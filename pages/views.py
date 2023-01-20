from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from . forms import ContactForm, AddProductForm, EditProfileForm
from . models import Profile, Follow
from products.models import Product
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from discussion.models import Discuss
from discussion.models import Comment as DiscussComment
from products.views import Comment as ProductComment

def index(request):
    products_by_like = Product.objects.annotate(l_count = Count('likes')).order_by('-l_count')
    total_product = Product.objects.count()
    context = {
        'total_product': total_product, 
        'products_by_like': products_by_like[:8],
        }
    return render(request, "index.html", context)

def sell(request):
    return render(request, "sell.html")

class ContactView(SuccessMessageMixin, FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    success_message = 'Your message is received.'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def faq(request):
    return render(request,"faq.html")
def terms_n_conditions(request):
    return render(request,"terms_n_conditions.html")
def privacy_policy(request):
    return render(request,"privacy_policy.html")
def about(request):
    return render(request,"about.html")

class AddProductView(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'add_product.html'

class DeleteProductView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('designs')

def update_product(request, category_slug, product_id):
    context ={}
    obj = get_object_or_404(Product, category__slug = category_slug, id = product_id)

    if obj.seller.id == request.user.id:
        form = AddProductForm(request.POST or None, instance = obj)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/designs/{category_slug}/{product_id}")
 
        context["form"] = form
        context["obj"] = obj
        return render(request, "update_product.html", context)
    
    else:
        return HttpResponseRedirect(f"/designs/{category_slug}/{product_id}")

def ShowProfilePageView(request, profile_id, username):
    current_user = request.user

    profile = Profile.objects.get(id = profile_id, username = username)
    products = Product.objects.filter(seller = profile)

    total_like = 0
    for product_like in products:
        total_like += len(product_like.get_likes)

    posts = Discuss.objects.filter(author = profile)
    for post_like in posts:
        total_like += len(post_like.get_likes)  
    
    comments_profile = DiscussComment.objects.filter(user = profile)
    product_comments_profile = ProductComment.objects.filter(user = profile)
    for comment_like in comments_profile:
        total_like += len(comment_like.get_likes)
    for comment_dislike in comments_profile:
        total_like -= len(comment_dislike.get_dislikes)
    for comment_like in product_comments_profile:
        total_like += len(comment_like.get_likes)
    for comment_dislike in product_comments_profile:
        total_like -= len(comment_dislike.get_dislikes)

    following = False
    if request.user.is_authenticated:

        followers = profile.followers.filter(
        followed_by__id = request.user.id
        )
        if followers.exists():
            following = True

    # total_like_of_profile = 0
    # for product in products.values('likes'):
    #     if product['likes']:
    #         total_like_of_profile += product['likes']

    context = {
            'profile': profile,
            'products': products,
            'products_to_show': products[:8],
            'following': following,
            'total_like': total_like,
        }

    return render(request, 'profile.html', context)

def ShowSellersView(request):
    profiles_by_is_seller = Profile.objects.filter(is_seller = True)
    context = {
            'profiles_by_is_seller': profiles_by_is_seller
        }

    return render(request, 'sellers.html', context)


def ShowFavorite(request):
    current_user = request.user
    favorites = current_user.favorite_products.all()
    context = {
            'favorites': favorites,
        }

    return render(request, 'favorite.html', context)

def ShowLiked(request):
    current_user = request.user
    likes = current_user.liked_products.all()
    context = {
            'likes': likes,
        }

    return render(request, 'liked.html', context)


def edit_profile(request, profile_id, username):
    context ={}
    obj = get_object_or_404(Profile, id = profile_id, username = username)
    
    if obj.id == request.user.id:
        form = EditProfileForm(request.POST or None, instance = obj)
 

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/{profile_id}/{username}")
 
        context["form"] = form
        context["obj"] = obj
        return render(request, "edit_profile.html", context)
    
    else:
        return HttpResponseRedirect(f"/{profile_id}/{username}")

@login_required(login_url = "login")
def follow_or_unfollow_user(request, user_id):
    if user_id == request.user.id:
        return HttpResponseRedirect(f"/{user_id}/{request.user.username}")
    
    else:

        followed = get_object_or_404(Profile, id=user_id)
        followed_by = get_object_or_404(Profile, id=request.user.id)

        follow, created = Follow.objects.get_or_create(
            followed=followed,
            followed_by=followed_by
        )

        if created:
            followed.followers.add(follow)

        else:
            followed.followers.remove(follow)
            follow.delete()

        return HttpResponseRedirect(f"/{user_id}/{followed.username}")

def products_profile(request, profile_id, username):
    profile = Profile.objects.get(id = profile_id, username = username)
    products = Product.objects.filter(seller = profile)
    context = {
            'profile': profile,
            'products': products,
        }

    return render(request, 'products_profile.html', context)

def profile_account(request, profile_id, username):
    profile = Profile.objects.get(id = profile_id, username = username)
    context = {
            'profile': profile,
        }
    return render(request, 'profile_account.html', context)

# Create your views here.
