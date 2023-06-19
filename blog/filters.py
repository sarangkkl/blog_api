from django_filters import rest_framework as filters
from .models import Post


# We create filters for each field we want to be able to filter on
class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    body = filters.CharFilter(lookup_expr='icontains')
    
    author__username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'body', 'author__username']

