from .models import Post
from .serializers import PostSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from core.utls import response_structure
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from rest_framework.generics import RetrieveUpdateDestroyAPIView


# Create your views here.

class PostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get(self, request,pk=None):
        """
            This method is used to get all the posts or a single post
            also it can be used to filter the posts by title, author name or body
            example url: /posts/?title=example&author=john&body=test
        """
        if pk:
            try:
                post            = Post.objects.get(pk=pk)
                serializer      = PostSerializer(post)
                return Response(response_structure(serializer.data, 200, 'Post retrieved successfully', False))
            except Post.DoesNotExist:
                return Response(response_structure(None, 404, 'Post not found', True))
        else:
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
                serializer = PostSerializer(posts, many=True)
                return Response(response_structure(serializer.data, 200, 'Posts retrieved successfully', False))
        
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(response_structure(serializer.data, 201, 'Post created successfully', False))
    
    def put(self, request, pk):
        
        try:
            saved_post = Post.objects.get(pk=pk)
            try:
                self.check_object_permissions(request, saved_post)
            except:
                return Response(response_structure(None, 401, 'Unauthorized', True))
            data = request.data
            serializer = PostSerializer(instance=saved_post, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(response_structure(serializer.data, 200, 'Post updated successfully', False))
        except:
            return Response(response_structure(None, 404, 'Post not found', True))
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            try:
                self.check_object_permissions(request, post)
            except:
                return Response(response_structure(None, 401, 'Unauthorized', True))
            post.delete()
            return Response(response_structure(None, 204, 'Post deleted successfully', False))
        except:
            return Response(response_structure(None, 404, 'Post not found', True))
