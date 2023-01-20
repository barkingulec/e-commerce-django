from django.shortcuts import render
from . models import Discuss, Comment
from pages.models import Profile
from django.template.defaulttags import register
from django.http import HttpResponseRedirect
from . forms import CommentForm, AddPostForm
from products.models import Product
from django.db.models import Count
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from products.views import Comment as ProductComment

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

@register.filter
def subtract(value, arg):
    return value - arg

def discuss_list(request):
    current_user = request.user

    posts = Discuss.objects.all()
    
    total_like_list = {}
    for post in posts:
        singlePost = Discuss.objects.get(id = post.id)
        total_like = singlePost.likes.all().count()
        total_like_list[post] = total_like

    if request.GET.get('newest_to_oldest') == 'Newest to Oldest':
        posts = posts.order_by('-date')
    if request.GET.get('most_liked') == 'Most Liked':
        posts = Discuss.objects.annotate(l_count = Count('likes')).order_by('-l_count')
    add_post = None
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            add_post = form.save(commit=False)
            #add_post.name = add_post["name"]
            #add_post.description = add_post["description"]
            add_post.author = Profile.objects.get(id = current_user.id)
            #add_post.name = slugify(add_post.name)
            add_post.save()
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return redirect(add_post)
    else:
        form = AddPostForm()

    context = {
        'posts': posts,
        'total_like_list': total_like_list,
        'form': form,
        'add_post': add_post,
    }
    return render(request, 'discussion.html', context)

def post_detail(request, post_id, post_name):
    current_user = request.user

    post = Discuss.objects.get(id = post_id, name = post_name)

    profile = post.author
    posts = Discuss.objects.filter(author = profile)
    products = Product.objects.filter(seller = profile)
    comments_profile = Comment.objects.filter(user = profile)
    product_comments_profile = ProductComment.objects.filter(user = profile)

    total_like_of_profile = 0
    for post_like in posts:
        total_like_of_profile += len(post_like.get_likes)
    for product_like in products:
        total_like_of_profile += len(product_like.get_likes)
    for comment_like in comments_profile:
        total_like_of_profile += len(comment_like.get_likes)
    for comment_dislike in comments_profile:
        total_like_of_profile -= len(comment_dislike.get_dislikes)
    for comment_like in product_comments_profile:
        total_like_of_profile += len(comment_like.get_likes)
    for comment_dislike in product_comments_profile:
        total_like_of_profile -= len(comment_dislike.get_dislikes)

    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = Profile.objects.get(id = current_user.id)
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm()


    total_like = post.likes.all().count()
    if current_user.is_authenticated:
        fav_post = current_user.favorite_discuss.all()
        like_post = current_user.liked_discuss.all()
    else:
        fav_post = None
        like_post = None

    context = {
        'post': post,
        'profile': profile,
        'fav_post': fav_post,
        'like_post': like_post,
        'comment_form': form,
        'comments': comments,
        'total_like': total_like,
        'total_like_of_profile': total_like_of_profile,
        }
    return render(request, 'post.html', context)

def post_delete_comment(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        post = Discuss.objects.get(id = post_id)
        comments = Comment.objects.filter(post=post)
        comment = comments.get(id = request.POST["comment_id"])
        comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, post_name, pk, *args, **kwargs):
        post = Discuss.objects.get(pk = post_pk, name = post_name)
        parent_comment = Comment.objects.get(pk = pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = Profile.objects.get(id = request.user.id)
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AddCommentLike(LoginRequiredMixin, View):
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

class AddCommentDislike(LoginRequiredMixin, View):
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
