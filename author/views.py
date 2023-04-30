from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import AuthorSerializer
from .authentification import create_access_token, create_refresh_token, decode_refresh_token
from django.contrib.auth import authenticate


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthorSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthorSerializer

    def post(self, request):
        if {'username', 'password'}.issubset(request.data):
            author = authenticate(request, username=request.data['username'], password=request.data['password'])
            if author is None:
                return JsonResponse({'Status': False, 'error': 'Invalid credentials!'},
                                    status=status.HTTP_403_FORBIDDEN)
            access_token = create_access_token(author.id)
            refresh_token = create_refresh_token(author.id)
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            response.data = {'token': access_token}
            return response
        return JsonResponse({'Status': False, 'error': 'Invalid credentials!'},
                            status=status.HTTP_403_FORBIDDEN)


class RefreshAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        author_id = decode_refresh_token(refresh_token)
        access_token = create_access_token(author_id)
        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }
        return response
