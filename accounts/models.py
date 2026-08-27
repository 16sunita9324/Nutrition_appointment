from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    # Connect Profile to Django's built-in User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Client onboarding fields
    # These are ready for the future client form.
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username

    @property
    def is_admin(self):
        return (
            self.user.is_staff
            or self.user.is_superuser
        )

    @property
    def is_client(self):
        return not self.user.is_staff


# ==========================================
# AUTOMATICALLY CREATE PROFILE
# ==========================================

@receiver(post_save, sender=User)
def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
):

    if created:
        Profile.objects.create(
            user=instance
        )


# ==========================================
# AUTOMATICALLY SAVE PROFILE
# ==========================================

@receiver(post_save, sender=User)
def save_user_profile(
    sender,
    instance,
    **kwargs
):

    if hasattr(instance, 'profile'):
        instance.profile.save()