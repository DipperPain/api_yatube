
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from posts.models import Group, Post

from .serializers import CommentSerializer, PostSerializer, GroupSerializer

from rest_framework.permissions import IsAuthenticated




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrive(self, request):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(data=post)
        serializer.is_valid()
        return Response(data=serializer.data)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        return super().perform_update(serializer)




class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
