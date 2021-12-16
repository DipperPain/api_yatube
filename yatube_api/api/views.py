
from django.http import request
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from posts.models import Comment, Group, Post
from rest_framework import status

from .serializers import CommentSerializer, PostSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        if self.request.user.is_authenticated:
            serializer = PostSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if request.method == 'GET':
            post = get_object_or_404(Post, pk=pk)
            serializers = PostSerializer(data=post)
            if serializers.is_valid():
                return Response(
                    data=serializers.data, status=status.HTTP_200_OK)

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

    @action(
        methods=['get', 'post'], detail=True, permission_classes=[IsAuthenticated]
    )
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)

        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            if self.request.user.is_authenticated:
                
                serializer = CommentSerializer(data=self.request.data)
                if serializer.is_valid():
                    serializer.validated_data
                    serializer.save(author=self.request.user)
                    return Response(
                        data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):

        return Response(
            request.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentiewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, pk=None, id=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        comment = post.comments.filter(pk=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def perform_destroy(self, instance, pk=None, id=None):
        if self.request.method == 'DELETE':

            if self.request.user.is_authenticated:
                instance.delete()
            else: 
                return Response(status=status.HTTP_204_NO_CONTENT)
        return super().perform_destroy(instance)

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
