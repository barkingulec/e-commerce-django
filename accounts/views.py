from django.shortcuts import render, redirect
from . forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from products.models import Product
from pages.models import Profile
from django.contrib.auth.models import User
from discussion.models import Discuss


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('index')
                    else:
                        messages.info(request, 'Account is disabled')
                else:
                    messages.info(request, 'Username or password is wrong')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

def user_register(request):

    if request.user.is_authenticated:
        return redirect('index')

    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                #new_user = form.save()
                # s         
                usuario = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']

                u = User.objects.create_user(username=usuario,email=email,password=password1)
                u.save()

                #add user profile
                user_profile = Profile(user=u, username=usuario)
                user_profile.save()
                # e
                messages.success(request, 'Account has been created, You can LOGIN')
                new_user = authenticate(username=usuario,
                                    password=password1,
                                    )
                login(request, new_user)
                return HttpResponseRedirect(f"/{u.id}/{usuario}")
    
        else:
            form = RegisterForm()

        return render(request, 'register.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def user_dashboard(request):
    current_user = request.user

    favorites = current_user.favorite_products.all()
    likes = current_user.liked_products.all()

    context = {
        'favorites': favorites,
        'likes': likes,
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def add_to_favorite(request):
    product_id = request.POST['product_id']
    user_id = request.POST['user_id']
    product = Product.objects.get(id = product_id)
    user = User.objects.get(id = user_id)
    product.favorites.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def add_to_liked(request):
    product_id = request.POST['product_id']
    user_id = request.POST['user_id']
    product = Product.objects.get(id = product_id)
    user = User.objects.get(id = user_id)
    product.likes.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_favorite(request):
    product = Product.objects.get(id = request.POST['product_id'])
    user = User.objects.get(id = request.POST['user_id'])
    product.favorites.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_liked(request):
    product = Product.objects.get(id = request.POST['product_id'])
    user = User.objects.get(id = request.POST['user_id'])
    product.likes.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def post_add_to_favorite(request):
    post_id = request.POST['post_id']
    user_id = request.POST['user_id']
    post = Discuss.objects.get(id = post_id)
    user = User.objects.get(id = user_id)
    post.favorites.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def post_add_to_liked(request):
    post_id = request.POST['post_id']
    user_id = request.POST['user_id']
    post = Discuss.objects.get(id = post_id)
    user = User.objects.get(id = user_id)
    post.likes.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_remove_from_favorite(request):
    post = Discuss.objects.get(id = request.POST['post_id'])
    user = User.objects.get(id = request.POST['user_id'])
    post.favorites.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_remove_from_liked(request):
    post = Discuss.objects.get(id = request.POST['post_id'])
    user = User.objects.get(id = request.POST['user_id'])
    post.likes.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Create your views here.
