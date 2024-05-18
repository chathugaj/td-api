from rest_framework import generics, permissions

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentDetailSerializer
from td_api.permissions import IsOwnerOrReadOnly


class CommentList(generics.ListCreateAPIView):
    """
    Facilitates the list and create comment API endpoints
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """Creates a comment"""
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """Facilitates get, update, delete a specific comments"""
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
