from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import User, Follow
from .serializers import FollowSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        page = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowSerializer(page, many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscription = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response({'error': 'Нельзя подписываться на себя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif subscription.exists():
                return Response({'error': 'Вы уже подписаны на пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not subscription.exists():
                return Response({'error': 'Вы не подписаны на пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
