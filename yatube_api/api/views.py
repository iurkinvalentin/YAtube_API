from rest_framework import viewsets, filters
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404


from .permissions import IsOwnerOrReadOnly, ReadOnly
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)


class FollowViewSet(viewsets.ModelViewSet):
    """Позволяет управлять подписками."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    """Cоздание, чтение, обновление и удаление постов"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Переопределяет метод создания поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп. Поддерживает только операции чтения."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Поддерживает создание, чтение, обновление и удаление комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,]

    def get_queryset(self):
        """Возвращает набор данных, отфильтрованный по идентификатору поста."""
        post_id = self.kwargs.get('post_id')
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            return post.comments.all()
        return super().get_queryset()

    def perform_create(self, serializer):
        """Переопределяет метод создания комментария."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)
