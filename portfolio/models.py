from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('SW', 'Software'),
        ('EL', 'Electronics'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='SW')

    description = models.TextField()

    detailed_content = RichTextField(blank=True, null=True)

    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    tech_stack = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.project.title}"