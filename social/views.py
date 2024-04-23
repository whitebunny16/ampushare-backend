from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import Buddy
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer

"""
Post View
"""


@extend_schema(
    request=PostSerializer,
    methods=["POST"]
)
@api_view(['GET', 'POST'])
def posts(request, post_id=None):
    """
    List all posts, or create a new post
    :param request:
    :param post_id:
    :return:
    """
    if request.method == 'GET':
        following_users = list(Buddy.objects.filter(follower=request.user).values_list('following', flat=True))
        following_users.append(request.user.id)

        # Filter the posts based on the users that the current user follows
        posts = Post.objects.filter(user__in=following_users)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=PostSerializer,
    methods=["PUT"]
)
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    """
    Retrieve, update or delete a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Like View
"""


@extend_schema(
    request=LikeSerializer,
    methods=["POST"]
)
@api_view(['POST', 'DELETE'])
def like_post_detail(request, post_id):
    """
        Like or unlike a post
        :param request:
        :param post_id:
        :return:
        """
    if request.method == 'POST':
        like_exists = Like.objects.filter(user=request.user.id, post=post_id).exists()
        if like_exists:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like_data = {'user': request.user.id, 'post': post_id}
        serializer = LikeSerializer(data=like_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post_like_instance = get_object_or_404(Like, user=request.user.id, post=post_id)
        post_like_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Comment View
"""


# @extend_schema(
#     request=CommentSerializer,
#     methods=["POST"]
# )
@api_view(['GET', 'POST'])
def post_comments(request, post_id):
    """
    Retrieve all comments for a post or add a new comment
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("Inside POST")

        print("post_comments", post_id)
        print("request.user", request.user)
        print("request.user ID", request.user.id)

        comment_data = {'user': request.user.id, 'post': post_id, 'text': request.data.get('text')}

        print(comment_data)

        serializer = CommentSerializer(data=comment_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def comment_detail(request, post_id, comment_id):
    """
    Retrieve a specific comment or delete a comment
    :param request:
    :param post_id:
    :param comment_id:
    :return:
    """
    comment = get_object_or_404(Comment, id=comment_id, post=post_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user != comment.user:
            return Response({"detail": "Not authorized to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
