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
            'institution': 'Language Learning High School "EG Geo Milev"',
            'degree': 'Primary Language: German; Secondary Language: English',
            'year': '2020 - 2025',
            'description': 'Elite Language Learning High School in Dobrich, Bulgaria',
            'icon': 'fas fa-school'
        },
        {
            'institution': 'Software University(SoftUni)',
            'degree': 'Software Engineer with Python',
            'year': '2022 - 2025',
            'description': 'Python Basics; Python Fundamentals; Python Advanced; DataBases; Python Web',
            'icon': 'fas fa-graduation-cap'
        },
        {
            'institution': 'Technical University Varna',
            'degree': 'Information and Communication Technology',
            'year': '2025 - 2029',
            'description': 'One of the best Universities in Bulgaria',
            'icon': 'fas fa-university'
        }
    ]

    certificates_data = [
        {
            'title': 'Python Fundamentals',
            'issuer': 'SoftUni',
            'year': '2024',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/221698/c2c87d1e'
        },
        {
            'title': 'Python Advanced',
            'issuer': 'SoftUni',
            'year': '2024',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/227651/e1ebd439'
        },
        {
            'title': 'Python OOP',
            'issuer': 'SoftUni',
            'year': '2024',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/231822/70cd1167'
        },
        {
            'title': 'Python ORM',
            'issuer': 'SoftUni',
            'year': '2025',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/240810/94c700fb'
        },
        {
            'title': 'PostgreSQL',
            'issuer': 'SoftUni',
            'year': '2025',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/241385/21b4f6c5'
        },
        {
            'title': 'Django Basics',
            'issuer': 'SoftUni',
            'year': '2025',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/246234/caf6a2c4'
        },
        {
            'title': 'Django Advanced',
            'issuer': 'SoftUni',
            'year': '2025',
            'color': 'primary',
            'url': 'https://softuni.bg/certificates/details/248897/5cb379ca'
        },
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
