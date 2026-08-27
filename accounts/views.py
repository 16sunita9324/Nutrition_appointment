from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from .forms import RegisterForm


# ==========================================
# HOME
# ==========================================

def home(request):

    return render(
        request,
        'accounts/home.html'
    )
def about(request):

    return render(
        request,
        'accounts/about.html'
    )
def contact(request):

    return render(
        request,
        'accounts/contact.html'
    )


# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            # Create the User
            user = form.save()

            # Login the new user
            login(request, user)

            # Staff/admin users go to the admin dashboard
            if user.is_staff:
                return redirect('appointments:admin_dashboard')

            # Regular users go to home
            return redirect('accounts:home')

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check username and password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Login successful
            login(request, user)

            # Staff/admin users go to the admin dashboard
            if user.is_staff:
                return redirect('appointments:admin_dashboard')

            return redirect('accounts:home')

        else:

            # Login failed
            return render(
                request,
                'accounts/login.html',
                {
                    'error':
                        'Invalid username or password.'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    return redirect('accounts:home')

# ==========================================
# CLIENT PROFILE (READY FOR FUTURE FORM)
# ==========================================

def client_profile(request):
    """Placeholder route for the future client onboarding form.

    The separate client form is intentionally not shown yet. The route is
    kept now so the appointment flow can later become:
    Login -> Client Form -> Book Appointment, without changing appointment URLs.
    """
    if request.user.is_authenticated:
        return redirect('accounts:home')
    return redirect('accounts:login')
