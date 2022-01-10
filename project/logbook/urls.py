from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('export/<slug:slug>/', views.export_logbook_csv, name='export_logbook_csv'),
]
