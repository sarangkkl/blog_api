from django.urls import path
from .views import PostUpdateViewDestroy,ListCreateAPIView

urlpatterns = [
    path('posts', ListCreateAPIView.as_view(), name='posts'),
    path('posts/<int:pk>', PostUpdateViewDestroy.as_view(), name='posts_update_delete'),
]