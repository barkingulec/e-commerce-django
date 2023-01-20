from django.urls import path
from . views import discuss_list, post_detail, post_delete_comment, CommentReplyView, AddCommentLike, AddCommentDislike

urlpatterns = [
    path('', discuss_list, name="discuss_list"),
    path('<int:post_id>/<str:post_name>', post_detail, name="post_detail"),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('<int:post_pk>/<str:post_name>/comment/<int:pk>/reply', CommentReplyView.as_view(), name="comment_reply"),
    path('post_delete_comment', post_delete_comment, name="post_delete_comment"),
    #path("add_post/", AddPostView.as_view(), name="add_post"),
]