from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),
      path(
            'about/',
            views.about,
            name='about'
        ),
          path(
                'contact',
                views.contact,
                name='contact'
            ),

    # Login
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # Register
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # Logout
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Future client onboarding form
    path(
        'client-profile/',
        views.client_profile,
        name='client_profile'
    ),

]