from django.shortcuts import render
from .models import Project


def home(request):
    """
    Renders the homepage.
    1. Fetches all projects from the PostgreSQL database.
    2. Passes them to the frontend template.
    """
    projects = Project.objects.all()

    # context is the dictionary of data passed to HTML
    context = {
        'projects': projects
    }

    return render(request, 'portfolio/index.html', context)