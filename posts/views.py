from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, pagination, permissions

from td_api.pagination import StandardResultsSetPagination
from td_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    Returns a list of posts
    """
    serializer_class = PostSerializer

    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    pagination_class = StandardResultsSetPagination
    filterset_fields = [
        'likes__owner__profile',
        'owner__profile',
        'slug'
    ]
    search_fields = [
        'owner__username',
        'title',
        'sub_title'
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__creat   ed_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateAPIView):
    """
    Handles a specific post with a given id
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly|permissions.IsAdminUser]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
