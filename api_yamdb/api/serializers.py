import datetime as dt
from django.db.models import Q

from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category, Comment, Genre, Review, User, Title, CHOICES_ROLES
)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.SlugField(required=True)
    role = serializers.ChoiceField(
        choices=CHOICES_ROLES, required=False, default='user'
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User
        ordering = ['id']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            username = data['username']
            email = data['email']
            if User.objects.filter(
                Q(username=username) | Q(email=email)
            ).exists():
                raise serializers.ValidationError(
                    'User and email is required to been unique',
                    status.HTTP_400_BAD_REQUEST
                )
        return data


class TokenRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.SlugField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=200, required=True
    )
    username = serializers.CharField(
        max_length=60, required=True
    )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description',
            'category', 'genre'
        )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request']
                    .parser_context['kwargs']['title_id']
            )
            author = self.context['request'].user
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise serializers.ValidationError(
                    'Repeated review is not allowed',
                    status.HTTP_400_BAD_REQUEST
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

    def validate(self, data):
        if 'text' not in data.keys():
            result = dict.fromkeys(
                'text', 'This field is required!'
            )
            raise serializers.ValidationError(result)
        return data
