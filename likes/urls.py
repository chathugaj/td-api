from django.urls import path
from posts import views

urlpatterns = [
    path('likes/', views.PostList.as_view()),
]