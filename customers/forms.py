from django import forms
from django.core.validators import RegexValidator
from .models import Customer


class CustomerForm(forms.ModelForm):

    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must contain exactly 10 digits."
            )
        ],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone Number",
            "maxlength": "10",
            "inputmode": "numeric",
            "pattern": "[0-9]{10}"
        })
    )

    class Meta:
        model = Customer

        fields = "__all__"

        widgets = {

            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Customer Name"
            }),

            "company_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Owner Name"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "maxlength": "10"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),

            "gst": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GST Number",
                "maxlength": "30"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Location"
            }),
        }