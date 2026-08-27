from datetime import date

from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'appointment_time': forms.Select(),
            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Tell the nutritionist briefly what you would like help with...'
                }
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']

        if appointment_date < date.today():
            raise forms.ValidationError('Please select a future date.')

        if appointment_date.weekday() == 6:
            raise forms.ValidationError('Appointments are not available on Sundays.')

        return appointment_date

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            exists = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['Pending', 'Confirmed']
            ).exists()

            if exists:
                raise forms.ValidationError(
                    'This time slot is already booked. Please choose another slot.'
                )

        return cleaned_data
