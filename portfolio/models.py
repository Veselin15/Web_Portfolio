from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from PIL import Image
import os

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

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.image:
            self._resize_image(self.image, max_width=1200)

    def _resize_image(self, image_field, max_width=1200):
        try:
            path = image_field.path
            if os.path.exists(path):
                img = Image.open(path)

                if img.width > max_width:
                    output_size = (max_width, int(img.height * (max_width / img.width)))
                    img.thumbnail(output_size)

                    img.save(path, quality=85, optimize=True)
        except Exception as e:
            print(f"Error resizing image: {e}")
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Галерията може да е по-малка, например 800px
            self._resize_image(self.image, max_width=800)

    def _resize_image(self, image_field, max_width=1200):
        try:
            path = image_field.path
            if os.path.exists(path):
                img = Image.open(path)

                if img.width > max_width:
                    output_size = (max_width, int(img.height * (max_width / img.width)))
                    img.thumbnail(output_size)

                    img.save(path, quality=85, optimize=True)
        except Exception as e:
            print(f"Error resizing image: {e}")

    def __str__(self):
        return f"Image for {self.project.title}"


class Profile(models.Model):
    image = models.ImageField(upload_to='profile/')
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)

    def __str__(self):
        return "My Profile Settings"

    class Meta:
        verbose_name_plural = "Profile Settings"