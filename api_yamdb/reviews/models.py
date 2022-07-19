from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from api_yamdb.settings import ADMIN, MODERATOR, USER


CHOICES_ROLES = (ADMIN, MODERATOR, USER)


class User(AbstractUser):
    """Creation a custom user model with adds.
    This class is extended by `role`, `bio`, `created_at`,
    and `modified_at` fields.
    """

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES_ROLES = [
        (ADMIN, 'админ'),
        (MODERATOR, 'модератор'),
        (USER, 'юзер')
    ]
    username = models.CharField(
        unique=True,
        blank=True,
        null=False,
        max_length=100,
        help_text='Please type your username!'
    )
    email = models.EmailField(
        blank=True, null=False,
        unique=True,
        help_text='Please type your Email adress!'
    )
    role = models.CharField(
        blank=True, null=True,
        max_length=200,
        choices=CHOICES_ROLES,
        default=USER
    )
    bio = models.TextField(
        blank=True, null=True,
        help_text='Please, tell something about your self'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    code_approve = models.UUIDField(null=True)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('username', 'email')
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='name_email_constraint'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == ADMIN)

    @property
    def is_moderator(self):
        return (self.role == MODERATOR)


class Category(models.Model):
    """Creation a category name for content like movie, book, etc.
    """

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Creation a genre name for content."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Creation a title's object for content. """

    name = models.CharField(
        max_length=256, verbose_name='Название',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        null=True,
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(0)
        ],
        db_index=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='Genre_Title'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория',
        db_index=True
    )
    description = models.TextField(
        null=True,
        max_length=2000,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Creation a title name for a genre's object.
    wich is an inner bonded object to Genre and Title instances!
    """

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_genre_title'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Leaving a review mark to content"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_review'
    )
    text = models.CharField(
        max_length=2000,
        verbose_name='Отзыв',
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_review',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Creation a comment."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.CharField(
        max_length=2000,
        null=False,
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comment',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )
