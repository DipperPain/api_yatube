
from django.http import request
from rest_framework import serializers, viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from posts.models import Comment, Group, Post
from rest_framework import status

from .serializers import CommentSerializer, PostSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action, permission_classes


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = PostSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = PostSerializer(data=self.queryset, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrive(self, request, pk=None):
        if request.method == 'GET':
            post = get_object_or_404(Post, id=pk)
            serializer = PostSerializer(data=post)
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    
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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

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


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)