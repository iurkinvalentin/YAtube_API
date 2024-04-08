from django.shortcuts import get_object_or_404
from rest_framework import mixins, filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Позволяет управлять подписками."""

    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.followers.all()


class PostViewSet(viewsets.ModelViewSet):
    """Cоздание, чтение, обновление и удаление постов"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Переопределяет метод создания поста."""

        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп. Поддерживает только операции чтения."""

    permission_classes = [permissions.AllowAny]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Поддерживает создание, чтение, обновление и удаление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_post(self):
        """Вспомогательный метод для получения объекта поста."""

        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post

    def get_queryset(self):
        """Возвращает набор данных, отфильтрованный по идентификатору поста."""

        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """Переопределяет метод создания комментария."""

        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
