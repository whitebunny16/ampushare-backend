from django.urls import path

from .views import *

urlpatterns = [
    # Post
    path('posts', posts),
    path('posts/<str:post_id>', post_detail),

    # Like
    path('posts/<str:post_id>/like', like_post_detail),

    # Comment
    path('posts/<str:post_id>/comments', post_comments),
    path('posts/<str:post_id>/comments/<str:comment_id>', comment_detail),
]
