from django.urls import path
from .views import RegisterAPIView, LoginAPIView

app_name = 'api'

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view())
]