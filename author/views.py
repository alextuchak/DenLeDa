from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.http import JsonResponse
from rest_framework import status
from .serializers import AuthorSerializer
from .models import Author
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
                                    status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.serializer_class(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'Status': False, 'error': 'Invalid credentials!'},
                            status=status.HTTP_401_UNAUTHORIZED)
