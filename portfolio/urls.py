from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    # path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    # --- API Endpoint React ---
    path('api/data/', views.api_portfolio_data, name='api_data'),
]
