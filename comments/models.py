from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


class Comment(models.Model):
    """
    Represents a comment
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
