from django.urls import path

from comments.views import CommentList, CommentDetail

urlpatterns = [
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view())
]