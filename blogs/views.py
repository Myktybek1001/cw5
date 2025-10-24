from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer

@api_view(['GET', 'POST'])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.filter(is_published=True)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Только авторизованные могут создавать посты'}, status=403)

        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Пост не найден'}, status=404)

    if request.method == 'GET':
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    if request.user != post.author:
        return Response({'error': 'Вы не автор этого поста'}, status=403)

    if request.method == 'PUT':
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=204)

@api_view(['GET', 'POST'])
def comment_list_create(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Пост не найден'}, status=404)

    if request.method == 'GET':
        if request.user.is_authenticated:
            comments = post.comments.all()
        else:
            comments = post.comments.filter(is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Нужно войти, чтобы комментировать'}, status=403)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
