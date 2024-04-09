from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок пользователей."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        return value


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов в блоге."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к постам."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created', 'post']
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп, организующих посты по категориям."""

    class Meta:
        model = Group
        fields = '__all__'
