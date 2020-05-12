from .models import Review
from django import forms


class FormReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'email', 'text')

