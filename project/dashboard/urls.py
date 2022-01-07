from django.urls import path

from . import views

urlpatterns = [
    path('raw-24h/<slug:slug>/', views.graphs_raw_24h, name='ds_raw_24h'),
]
