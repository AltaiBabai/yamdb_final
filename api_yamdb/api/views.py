from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404


from rest_framework import (
    filters, viewsets, permissions, mixins
)
from reviews.models import (
    Category, Comment, Genre, Review, Title, User
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .pagination import ReviewPagination
from .serializers import (
    TitleListSerializer, TitleCreateSerializer, ReviewSerializer,
    CommentSerializer, CategorySerializer,
    GenreSerializer, UserSerializer
)
from .permissions import (
    ReadOnlyOrOwnerOrAllAdmins, ReadOnlyOrAdmins, OwnerOrAdmins
)
from .filters import TitleFilterSet


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    pagination_class = ReviewPagination
    permission_classes = (ReadOnlyOrAdmins,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    pagination_class = ReviewPagination
    permission_classes = (ReadOnlyOrAdmins,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('title_review__score')
    ).order_by('-id')
    pagination_class = ReviewPagination
    permission_classes = (ReadOnlyOrAdmins,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    permission_classes = (ReadOnlyOrOwnerOrAllAdmins,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(
            title__pk=title_id
        ).order_by('-id')
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        try:
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise ValidationError(
                'Reviews with this Title and Owner already exists.'
            )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = ReviewPagination
    permission_classes = (ReadOnlyOrOwnerOrAllAdmins,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        # new_queryset = Comment.objects.filter(
        #   review__pk=review_id
        # ).filter(review__title__pk=title_id).order_by('-id')
        return Comment.objects.filter(
            review__pk=review_id
        ).filter(review__title__pk=title_id).order_by('-id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review, id=review_id, title=title
        )
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    pagination_class = ReviewPagination
    permission_classes = (OwnerOrAdmins,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_patch_user(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if self.request.method == 'GET':
            serializers = self.get_serializer(user)
            return Response(serializers.data)
        if self.request.method == 'PATCH':
            serializers = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializers.is_valid(raise_exception=True)
            serializers.save(role=user.role)
        return Response(serializers.data)
