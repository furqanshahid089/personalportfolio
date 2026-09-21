"""Forms for the personal portfolio app."""

from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """Validated contact form backed by the ContactMessage model."""

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Please enter a message of at least 10 characters."
            )
        return message
