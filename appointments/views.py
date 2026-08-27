from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from .forms import AppointmentForm
from .models import Appointment


def staff_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('appointments:admin_login')
        if not request.user.is_staff:
            return redirect('appointments:admin_login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def client_profile_complete(user):
    """Central place for the future client-form requirement.

    For now CLIENT_FORM_REQUIRED is False, so registration/login continues
    to work exactly as it does today. When the client form is added, the
    flag can be enabled and this check can be expanded without changing
    appointment booking logic.
    """
    if not getattr(settings, 'CLIENT_FORM_REQUIRED', False):
        return True

    profile = getattr(user, 'profile', None)
    if profile is None:
        return False

    # Future client form fields can be added here.
    return bool(
        profile.phone and
        profile.address and
        profile.date_of_birth
    )


@login_required
def book_appointment(request):
    # Future flow: Login -> Client Form -> Book Appointment.
    # Currently the client form is not required yet.
    if not client_profile_complete(request.user):
        messages.info(request, 'Please complete your client profile before booking an appointment.')
        return redirect('accounts:client_profile')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            messages.success(
                request,
                'Appointment request submitted successfully. Please wait for confirmation.'
            )
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    if request.method == 'POST':
        if appointment.status in ['Pending', 'Confirmed']:
            appointment.status = 'Cancelled'
            appointment.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Your appointment has been cancelled.')
        else:
            messages.warning(request, 'This appointment cannot be cancelled.')

    return redirect('appointments:my_appointments')


# ==============================
# CUSTOM NUTRITIONIST LOGIN
# ==============================

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('appointments:admin_dashboard')

    if request.method == 'POST':
        from django.contrib.auth import authenticate, login

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('appointments:admin_dashboard')

        return render(request, 'appointments/admin_login.html', {
            'error': 'Invalid nutritionist/admin username or password.'
        })

    return render(request, 'appointments/admin_login.html')


@login_required
def admin_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('appointments:admin_login')


# ==============================
# ADMIN / NUTRITIONIST DASHBOARD
# ==============================

@staff_required
def admin_dashboard(request):
    status_filter = request.GET.get('status', 'All')
    appointments = Appointment.objects.select_related('user').order_by(
        'appointment_date', 'appointment_time'
    )

    if status_filter in dict(Appointment.STATUS_CHOICES):
        appointments = appointments.filter(status=status_filter)

    from django.utils import timezone

    context = {
        'appointments': appointments,
        'status_filter': status_filter,
        'total_count': Appointment.objects.count(),
        'pending_count': Appointment.objects.filter(status='Pending').count(),
        'confirmed_count': Appointment.objects.filter(status='Confirmed').count(),
        'completed_count': Appointment.objects.filter(status='Completed').count(),
        'cancelled_count': Appointment.objects.filter(status='Cancelled').count(),
        'rejected_count': Appointment.objects.filter(status='Rejected').count(),
        'today': timezone.localdate(),
    }
    return render(request, 'appointments/admin_dashboard.html', context)


@staff_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    # Only pending appointments can be rejected from this page.
    if appointment.status != 'Pending':
        messages.warning(request, 'Only pending appointments can be rejected.')
        return redirect('appointments:admin_dashboard')

    if request.method == 'POST':
        rejection_message = request.POST.get('rejection_message', '').strip()

        if not rejection_message:
            return render(request, 'appointments/reject_appointment.html', {
                'appointment': appointment,
                'error': 'Please enter a reason for rejecting the appointment.'
            })

        appointment.status = 'Rejected'
        appointment.rejection_message = rejection_message
        appointment.save(update_fields=['status', 'rejection_message', 'updated_at'])

        messages.success(
            request,
            f"Appointment for {appointment.user.username} has been rejected."
        )
        return redirect('appointments:admin_dashboard')

    return render(
        request,
        'appointments/reject_appointment.html',
        {'appointment': appointment}
    )


@staff_required
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)

    allowed_statuses = {'Confirmed', 'Completed', 'Cancelled', 'Pending'}

    if request.method == 'POST' and status in allowed_statuses:
        appointment.status = status
        appointment.save(update_fields=['status', 'updated_at'])
        messages.success(
            request,
            f"Appointment for {appointment.user.username} marked as {status}."
        )

    return redirect('appointments:admin_dashboard')
