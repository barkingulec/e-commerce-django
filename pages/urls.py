from django.urls import path
from . import views
from . views import ContactView, AddProductView, ShowProfilePageView, update_product, ShowFavorite, ShowLiked, edit_profile, follow_or_unfollow_user, products_profile, DeleteProductView, profile_account

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicons/favicon.ico'))),
    path("", views.index, name="index"),
    path("sell/", views.sell, name="sell"),
    path("sellers/", views.ShowSellersView, name="sellers"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("terms-and-conditions/", views.terms_n_conditions, name="terms_n_conditions"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path('<int:profile_id>/<str:username>', ShowProfilePageView, name='show_profile_page'),
    path("add_product/", AddProductView.as_view(), name="add_product"),
    path('designs/update/<slug:category_slug>/<int:product_id>', update_product, name="update_product"),
    path('designs/delete/<int:pk>', DeleteProductView.as_view(), name="delete_product"),
    path("favorite/", ShowFavorite, name="favorite_page"),
    path("liked/", ShowLiked, name="liked_page"),
    path("edit/<int:profile_id>/<str:username>", edit_profile, name="edit_profile"),
    path('follow_or_unfollow/<int:user_id>', follow_or_unfollow_user, name='follow_or_unfollow_user'),
    path('<int:profile_id>/<str:username>/products', products_profile, name='products_profile'),
    path('edit/<int:profile_id>/<str:username>/account', profile_account, name='profile_account'),
]