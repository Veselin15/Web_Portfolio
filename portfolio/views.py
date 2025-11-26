from django.shortcuts import render, get_object_or_404
from .models import Project


def home(request):
    """
    Renders the homepage with separated project categories.
    """
    # Fetch projects by category
    software_projects = Project.objects.filter(category='SW')
    electronics_projects = Project.objects.filter(category='EL')

    # Static data for Education (No DB needed as discussed)
    education_data = [
        {
            'institution': 'Technical University',
            'degree': 'BSc Computer Science',
            'year': '2019 - 2023',
            'description': 'Algorithms, C++, OOP, Mathematics.',
            'icon': 'fas fa-graduation-cap'
        },
        # Add more items here...
    ]

    # Static data for Certificates
    certificates_data = [
        {
            'title': 'Python Advanced',
            'issuer': 'SoftUni',
            'year': '2023',
            'color': 'primary'
        },
        # Add more items here...
    ]

    context = {
        'software_projects': software_projects,
        'electronics_projects': electronics_projects,
        'education': education_data,
        'certificates': certificates_data,
    }

    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    """
    Renders the detailed page for a specific project (mainly for Electronics).
    """
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})
