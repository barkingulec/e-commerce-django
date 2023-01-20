from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="designs"),
    path('<slug:category_slug>/<int:product_id>', views.product_detail, name="product_detail"),
    path('categories/<slug:category_slug>', views.category_list, name="products_by_category"),
    path('tags/<slug:tag_slug>', views.tag_list, name="products_by_tag"),
    path('favorite', views.favorite_list, name="products_by_favorite"),
    path('liked', views.liked_list, name="products_by_liked"),
    path('search', views.search, name="search"),
    path('order_by_products', views.order_by_products, name="order_by_products"),
    path('delete_comment', views.delete_comment, name="delete_comment"),
    path('<int:product_id>/comment/<int:pk>/like', views.AddProductCommentLike.as_view(), name='product-comment-like'),
    path('<int:product_id>/comment/<int:pk>/dislike', views.AddProductCommentDislike.as_view(), name='product-comment-dislike'),
    path('<slug:category_slug>/<int:product_pk>/comment/<int:pk>/reply', views.ProductCommentReplyView.as_view(), name="product_comment_reply"),
]