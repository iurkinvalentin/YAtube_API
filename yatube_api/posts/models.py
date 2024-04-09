from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import MAX_LENGTH

User = get_user_model()


class Follow(models.Model):
    """Модель подписок пользователей."""

    user = models.ForeignKey(User, related_name='followers',
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    following = models.ForeignKey(User, related_name='followings',
                                  on_delete=models.CASCADE,
                                  verbose_name='Подписки')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        return f"{self.user.username} follows {self.following.username}"


class Group(models.Model):
    """Модель для группировки постов."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title[:MAX_LENGTH]


class Post(models.Model):
    """Модель для публикации постов."""

    group = models.ForeignKey('Group', on_delete=models.SET_NULL,
                              null=True, blank=True)
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta:
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:MAX_LENGTH]


class Comment(models.Model):
    """Модель для комментариев к постам."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        preview_text = self.text[:MAX_LENGTH]
        return (
            f'Комментарий от {self.author.username} к '
            f'"{self.post.title}": "{preview_text}"'
        )
