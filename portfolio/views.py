from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import Project

from .portfolio_data import EDUCATION_DATA, CERTIFICATES_DATA


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
                subject = f"Portfolio Message from {name}"
                full_message = f"Sender Name: {name}\nSender Email: {email}\n\nMessage:\n{message}"

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

    # 1. Dynamic Data (from Database)
    software_projects = Project.objects.filter(category='SW')
    electronics_projects = Project.objects.filter(category='EL')

    # 2. Static Data (from portfolio_data.py)
    context = {
        'software_projects': software_projects,
        'electronics_projects': electronics_projects,
        'education': EDUCATION_DATA,
        'certificates': CERTIFICATES_DATA,
    }

    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})