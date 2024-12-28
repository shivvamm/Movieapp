from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count

class PostPagination(PageNumberPagination):
    page_size = 10  # Customize the page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListView(APIView):
    pagination_class = PostPagination

    def get(self, request, *args, **kwargs):
        # Fetch posts with comment count, ordered by timestamp
        
        posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-timestamp')

        # Paginate the posts
        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(posts, request)
        
        # Serialize the data
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
