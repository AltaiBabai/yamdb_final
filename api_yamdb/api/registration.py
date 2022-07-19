from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import TokenRequestSerializer, TokenSerializer


@api_view(['POST'])
def create_user(request):
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, is_new = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email'])
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user.code_approve = uuid.uuid4()
    user.save()
    send_mail(
        'This is confirmation_code for '
        + user.username + ' take a token',
        'POST on http://127.0.0.1:8000/api/v1/auth/token/ '
        + 'with {"username":"'
        + user.username
        + '","confirmation_code":"'
        + str(user.code_approve) + '"}',
        'admin@api-yamdb.ru',
        [request.data['email']]
    )
    if is_new:
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(
        request.data, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def create_token(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.data['username']
        )
        if str(user.code_approve) != request.data['confirmation_code']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(refresh.access_token),
            }
        )
