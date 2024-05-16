from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from td_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    """
    Returns a list of posts
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @staticmethod
    def get(request):
        """
        Get the list of posts
        :param request: HTTP request
        :return: List of JSON objects with posts
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def post(request):
        """
        Create a post
        :param request: HTTP request with JSON object
        :return: JSON post with creation details
        """
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PostDetail(APIView):
    """
    Handles a specific post with a given id
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get a post for the specified id 'pk'
        :param request: HTTP request
        :param pk: Post id
        :return: Post details JSON object
        """
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of the post specified by the id
        :param request: HTTP request with JSON payload
        :param pk: Post id
        :return: Post details JSON object
        """
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """
        Delete the post object specified by the id
        :param request: HTTP request
        :param pk: Post id
        :return:
        """
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
