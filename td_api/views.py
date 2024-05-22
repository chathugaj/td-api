from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    REST_AUTH
)


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to the travler's diary API"
    })


from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, permissions


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'is_superuser']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# @api_view(['POST'])
# def logout_route(request):
#     response = Response()
#     response.set_cookie(
#         key=REST_AUTH.JWT_AUTH_COOKIE,
#         value='',
#         httponly=True,
#         expires='Thu, 01 Jan 1970 00:00:00 GMT',
#         max_age=0,
#         samesite=REST_AUTH.JWT_AUTH_SAMESITE,
#         secure=REST_AUTH.JWT_AUTH_SECURE,
#     )
#     response.set_cookie(
#         key=REST_AUTH.JWT_AUTH_REFRESH_COOKIE,
#         value='',
#         httponly=True,
#         expires='Thu, 01 Jan 1970 00:00:00 GMT',
#         max_age=0,
#         samesite=REST_AUTH.JWT_AUTH_SAMESITE,
#         secure=REST_AUTH.JWT_AUTH_SECURE,
#     )
#     return response
