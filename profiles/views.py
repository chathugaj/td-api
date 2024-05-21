from django.db.models import Count
from rest_framework import generics, filters
from rest_framework.views import APIView

from td_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    Returns a list of profiles
    Note: Profile creation is handled by the django signals
    """
    queryset = Profile.objects.annotate(
        post_count = Count('owner__post', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'post_count'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Handles API calls related to a specific profile id
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        post_count=Count('owner__post', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
