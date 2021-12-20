
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from posts.models import Group, Post
from rest_framework import status

from .serializers import CommentSerializer, PostSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if request.method == 'GET':
            serializer = PostSerializer(data=Post.objects.all(), many=True)
            serializer.is_valid()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrive(self, request, pk=None):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(data=post)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().perform_destroy(instance)

    @action(methods=['get', 'post'], detail=True,
            permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)

        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def retrieve(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            comments = self.get_queryset()
            comment = comments.get(id=self.kwargs.get('comment_id'))
            serializer = CommentSerializer(data=comment)
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_update(serializer)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        if request.method == 'GET':
            groups = Group.objects.all()
            serializer = GroupSerializer(data=groups, many=True)
            serializer.is_valid()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(Group, id=pk)
        posts = group.posts.all()
        serializer = PostSerializer(data=posts, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
