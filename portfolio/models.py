from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    # Category choices
    CATEGORY_CHOICES = [
        ('SW', 'Software'),
        ('EL', 'Electronics'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='SW')

    # Short description for the card
    description = models.TextField()

    # Full content for the internal page (Electronics projects)
    detailed_content = models.TextField(blank=True, null=True, help_text="Full details for the internal project page.")

    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    # External URL (GitHub for Software)
    url = models.URLField(blank=True, null=True, help_text="GitHub URL for Software or External Link")

    tech_stack = models.CharField(max_length=200, blank=True, null=True)

    # Timeline
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if the project is ongoing (Present).")

    # Slug for internal URLs (e.g., /project/my-robot-v1)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title