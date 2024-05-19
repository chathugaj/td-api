from django.contrib.auth.models import User
from django.db import models


class Report(models.Model):
    """
    Represents a user created report on content or a user
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=150, blank=True)
    message = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reason}' by {self.owner}"
