from django.http import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from td_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    Returns a list of profiles
    Note: Profile creation is handled by the django signals
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(APIView):
    """
    Handles API calls related to a specific profile id
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
