from rest_framework import generics, permissions

from td_api.pagination import StandardResultsSetPagination
from .models import Like
from .serializers import LikeSerializer
from td_api.permissions import IsOwnerOrReadOnly


class LikeList(generics.ListCreateAPIView):
    """
    Facilitates list and create for likes
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Get a like or delete a like by id
    """
    permission_classes = [IsOwnerOrReadOnly|permissions.IsAdminUser]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()