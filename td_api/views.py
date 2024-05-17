from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['GET', 'POST', 'PUT', 'DELETE'])
def root_route(request):
    return Response({
        "message": "Welcome to the travler's diary API"
    })
