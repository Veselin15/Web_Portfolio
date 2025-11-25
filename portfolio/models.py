from django.db import models
from django.db import models


class Project(models.Model):
    """
    Model representing a portfolio project.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tech_stack = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']  # Newest projects first

    def __str__(self):
        return self.title

