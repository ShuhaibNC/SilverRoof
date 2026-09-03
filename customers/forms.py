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

            # Showing Owner Name, but using existing company_name field
            "company_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Owner Name"
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

            "gst_number": forms.TextInput(attrs={
    "class": "form-control",
    "placeholder": "GST Number",
    "maxlength": "15"
}),

            "location": forms.Select(attrs={
                "class": "form-select"
            }),
        }