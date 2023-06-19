from .models import Post
from .serializers import PostSerializer 
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from core.utls import response_structure
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView



class PostUpdateViewDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'


    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance)
        return Response(response_structure(serializer.data, 200, 'Post retrieved successfully', False))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(response_structure(serializer.data, 200, 'Post updated successfully', False))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(response_structure(None, 200, 'Post deleted successfully', False))
    

class ListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get(self, request):
        """
            This method is used to get all the posts or a single post
            also it can be used to filter the posts by title, author name or body
            example url: /posts/?title=example&author=john&body=test
        """
        
        posts = Post.objects.all()
        query_params        = request.query_params
        title               = query_params.get('title', None)
        author_name         = query_params.get('author', None)
        body                = query_params.get('body', None)
        post_per_page       = query_params.get('post_per_page', None)
        page_number         = query_params.get('page_number', 1)
        if title:
            posts           = posts.filter(title__icontains=title)
        if author_name:
            try:
                author          = User.objects.get(username=author_name)
            except User.DoesNotExist:
                return Response(response_structure(None, 404, 'Author not found', True))
            posts           = posts.filter(author=author)
        if body:
            posts           = posts.filter(body__icontains=body)
        if post_per_page:
            paginated_posts     = Paginator(posts, post_per_page)
            total_page          = paginated_posts.num_pages
            if int(page_number) > total_page:
                return Response(response_structure(None, 404, 'Page not found', True))
            paginated_posts     = paginated_posts.get_page(page_number)
            serializer          = PostSerializer(paginated_posts, many=True)
            return Response(response_structure(serializer.data, 200, 'Posts retrieved successfully', False,total_page,page_number))
        else:
            serializer          = PostSerializer(posts, many=True)
            return Response(response_structure(serializer.data, 200, 'Posts retrieved successfully', False))
        

            
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
