from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """
    Represents a blog post.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    banner = models.ImageField('images/', default='default_post_zzidm6')
    body = models.TextField(max_length=5000, blank=True)
    gmap_location_tag = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title[0:100]}' by {self.owner}"
