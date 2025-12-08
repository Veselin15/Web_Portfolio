from django.contrib import admin
from .models import Project, ProjectImage, Profile  # <--- Добави Profile тук

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

# Добавяме това за Профила
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Profile.objects.exists()