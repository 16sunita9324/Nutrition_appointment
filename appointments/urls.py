from django.urls import path

from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('nutritionist-login/', views.admin_login, name='admin_login'),
    path('nutritionist-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/<int:pk>/reject/', views.reject_appointment, name='reject_appointment'),
    path('admin-dashboard/<int:pk>/status/<str:status>/', views.update_appointment_status, name='update_status'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
]
