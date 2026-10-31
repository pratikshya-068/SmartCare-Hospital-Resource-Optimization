from django.contrib import admin
from django.urls import path
from hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('patients/', views.patient_records, name='patient_records'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('beds/', views.bed_management, name='bed_management'),
    path('beds/<int:bed_id>/delete/', views.delete_bed, name='delete_bed'),
    path('beds/<int:bed_id>/toggle/', views.toggle_bed_status, name='toggle_bed_status'),
    path(
    'patients/<int:patient_id>/discharge/',
    views.discharge_patient,
    name='discharge_patient'
),
]