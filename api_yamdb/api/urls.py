from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet, CommentsViewSet, GenresViewSet,
    TitlesViewSet, ReviewsViewSet, UsersViewSet
)
from .registration import create_token, create_user


app_name = 'api'

router1 = DefaultRouter()  # version 1
router1.register(
    'categories', CategoriesViewSet, basename='categories'
)
router1.register('genres', GenresViewSet, basename='genres')
router1.register('titles', TitlesViewSet, basename='titles')
router1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/'
    '(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comments'
)
router1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/'
    '(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comments'
)
router1.register(
    r'users', UsersViewSet, basename='users'
)

urlpatterns = [
    path('v1/', include(router1.urls)),
    path('v1/auth/signup/', create_user),
    path('v1/auth/token/', create_token)
]
