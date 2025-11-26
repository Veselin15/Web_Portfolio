from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug based on title
