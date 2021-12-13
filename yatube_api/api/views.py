
from django.contrib.auth.models import Permission
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
                return Response(data=serializers.data, status=status.HTTP_200_OK)



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
        methods=['get'], detail=True, permission_classes=[IsAuthenticated]
    )
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)

        if request.method == 'GET':
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)
   


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):

        return Response(request.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentiewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, comment_id=None, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.filter(post=post).filter(pk=comment_id)

    def perform_update(self, serializer,  post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.filter(post=post).filter(pk=comment_id)        
        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().perform_update(serializer)

    def delete(self, request, post_id, comment_id):        
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.filter(post=post).filter(pk=comment_id)
        if self.request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



        