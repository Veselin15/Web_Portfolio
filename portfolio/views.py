from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project
from django.urls import reverse

def home(request):
    """
    Renders the homepage and handles the Contact Form.
    """
    # --- HANDLE CONTACT FORM ---
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            try:
                # Construct the email
                subject = f"Portfolio Message from {name}"
                full_message = f"Sender Name: {name}\nSender Email: {email}\n\nMessage:\n{message}"

                # Send email to yourself (EMAIL_HOST_USER)
                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect(reverse('home') + '#contact')

            except Exception as e:
                messages.error(request, f"Error sending message: {e}")
        else:
            messages.error(request, "Please fill in all fields.")

    # --- LOAD DATA FOR TEMPLATE ---
    software_projects = Project.objects.filter(category='SW')
    electronics_projects = Project.objects.filter(category='EL')

    # Static Data
    education_data = [
        {
            'institution': 'Technical University',
            'degree': 'BSc Computer Science',
            'year': '2019 - 2023',
            'description': 'Algorithms, C++, OOP.',
            'icon': 'fas fa-graduation-cap'
        },
        # ... other items ...
    ]

    certificates_data = [
        {
            'title': 'Python Advanced',
            'issuer': 'SoftUni',
            'year': '2023',
            'color': 'primary'
        },
        {
            'title': 'Django Advanced',
            'issuer': 'SoftUni',
            'year': '2025',
            'color': 'primary'
        },
        {
            'title': 'Postgre SQL',
            'issuer': 'SoftUni',
            'year': '2024',
            'color': 'primary'
        },
        {
            'title': 'DSD II Diplom',
            'issuer': 'Germany',
            'year': '2024',
            'color': 'primary'
        },
        {
            'title': 'Python Fundamentals',
            'issuer': 'SoftUni',
            'year': '2023',
            'color': 'primary'
        }
        # ... other items ...
    ]

    context = {
        'software_projects': software_projects,
        'electronics_projects': electronics_projects,
        'education': education_data,
        'certificates': certificates_data,
    }

    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})