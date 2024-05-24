from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from td_api.pagination import StandardResultsSetPagination
from td_api.serializers import UserSerializer


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to the travler's diary API"
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or added.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


