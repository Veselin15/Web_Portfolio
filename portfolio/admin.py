from django.contrib import admin
from .models import Project, ProjectImage

# Позволява добавяне на снимки вътре в страницата на проекта
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline] # <--- Свързваме галерията