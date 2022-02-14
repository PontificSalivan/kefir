from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.status import \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .models import Person
from .serializers import UserSerializer, PrivateUserSerializer, PrivateUserCreateSerializer, \
    PrivateUserUpdateSerializer, UserCurrentSerializer


class LoginApiView(APIView):

    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None or password is None:
            return Response({'error': 'Укажите имя пользователя и пароль'}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверные учетные данные, попробуйте снова'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)


class LogoutApiView(APIView):

    @permission_classes([IsAdminUser, IsAuthenticated])
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except:
            return Response({'error': 'Вы не залогинены'}, status=HTTP_404_NOT_FOUND)
        return Response("Вы успешно разлогинились", status=HTTP_200_OK)


class UsersApiView(APIView):

    @permission_classes([IsAdminUser, IsAuthenticated])
    def get(self, request):
        user = Person.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserCurrentApiView(APIView):

    @permission_classes([IsAdminUser, IsAuthenticated])
    def get(self, request):
        user = Person.objects.filter(user_id=request.auth.user_id)
        serializer = UserCurrentSerializer(user, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserUpdateApiView(APIView):

    @permission_classes([IsAdminUser, IsAuthenticated])
    def patch(self, request, user_id):
        user = get_object_or_404(Person, pk=user_id)
        token_user = request.user
        if not token_user.is_superuser and token_user.id != user_id:
            return Response(f"Вы пытаетесь изменить не свои данные, чтобы изменить свои введите "
                            f"ваш id = {token_user.id}", status=HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PrivateUserApiView(APIView):

    @permission_classes([IsAdminUser])
    def get(self, request):
        users = Person.objects.all()
        serializer = PrivateUserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @permission_classes([IsAdminUser, IsAuthenticated])
    def post(self, request):
        token_user = request.user
        if not token_user.is_superuser and token_user.id != int(request.data['user_id']):
            return Response(f"Вы пытаетесь создать не своего пользователя, чтобы его создать введите "
                            f"ваш id = {token_user.id}", status=HTTP_400_BAD_REQUEST)
        serializer = PrivateUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(PrivateUserCreateSerializer(user).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PrivateUserUpdateApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        questionnaire = Person.objects.filter(user_id=user_id)
        serializer = PrivateUserSerializer(questionnaire, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, user_id):
        user = get_object_or_404(Person, pk=user_id)
        serializer = PrivateUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(PrivateUserUpdateSerializer(user).data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(Person, pk=user_id)
        user.delete()
        return Response(f"Пользователь {user.name} удален", status=HTTP_204_NO_CONTENT)