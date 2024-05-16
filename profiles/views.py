from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from td_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    Returns a list of profiles
    Note: Profile creation is handled by the django signals
    """
    @staticmethod
    def get(request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Handles API calls related to a specific profile id
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Returns profile details object represented by the 'pk'
        :param request: HTTP request
        :param pk: Profile id
        :return: Profile details
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Updates the profile details represented by 'pk'. Returns updated profile details.
        :param request: Http request with the Profile JSON
        :param pk: Profile id
        :return: Updated profile JSON
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
