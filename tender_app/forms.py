from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Tender, ISODetail
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from typing import Dict, Any
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user, full_name=self.cleaned_data["full_name"]
            )
        return user

    def clean_email(self) -> str:
        """Validate email uniqueness."""
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                "placeholder": "Password",
            }
        ),
    )


class TenderUpdateForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ("GHS", "Ghanaian Cedi"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        ("CAD", "Canadian Dollar"),
    ]

    currency_of_payment = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            }
        ),
    )

    contract_amount = forms.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        required=False,
    )

    amount_to_be_paid = forms.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        required=False,
    )

    def clean(self) -> Dict[str, Any]:
        """Validate tender form data."""
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        closing_date = cleaned_data.get("closing_date")
        invitation_date = cleaned_data.get("invitation_date")

        if closing_date and invitation_date:
            if closing_date < invitation_date:
                self.add_error(
                    "closing_date",
                    "Closing date cannot be earlier than invitation date",
                )

        return cleaned_data

    def clean_closing_date(self):
        closing_date = self.cleaned_data["closing_date"]
        if closing_date < date.today():
            raise ValidationError("Closing date cannot be in the past")
        return closing_date

    class Meta:
        model = Tender
        fields = [
            "tender_number",
            "user",
            "description",
            "department",
            "status",
            "category_type",
            "invitation_date",
            "closing_date",
            "evaluation_date",
            "date_of_contract",
            "currency_of_payment",
            "contract_amount",
            "name_of_vendor_consultant",
            "date_of_po",
            "po_number",
            "date_of_sra_certification",
            "sra_certification_number",
            "date_of_payment_memo",
            "amount_to_be_paid",
            "file_name",
            "file_no",
        ]
        widgets = {
            "tender_number": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Tender Number",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Description",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                }
            ),
            "category_type": forms.Select(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                }
            ),
            "invitation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "closing_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "evaluation_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "date_of_contract": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "contract_amount": forms.NumberInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Contract Amount",
                }
            ),
            "name_of_vendor_consultant": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Name of Vendor/Consultant",
                }
            ),
            "date_of_po": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "po_number": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "PO Number",
                }
            ),
            "date_of_sra_certification": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "sra_certification_number": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "SRA Certification Number",
                }
            ),
            "date_of_payment_memo": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                }
            ),
            "amount_to_be_paid": forms.NumberInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "Amount to be Paid",
                }
            ),
            "file_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "File Name",
                }
            ),
            "file_no": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                    "placeholder": "File Number",
                }
            ),
        }
        labels = {
            "date_of_po": "Date of PO",
            "po_number": "PO Number",
            "date_of_sra_certification": "Date of SRA/CERTIFICATION",
            "sra_certification_number": "SRA/CERTIFICATION Number",
        }


class ISODetailForm(forms.ModelForm):
    LETTER_CHOICES = [
        ("Letter to PPA", "Letter to PPA"),
        ("RFQ Letter", "RFQ Letter"),
        ("Addendum", "Addendum"),
        ("Letter to CTRC", "Letter to CTRC"),
        ("Letter to Landlord", "Letter to Landlord"),
        ("Response to CTRC", "Response to CTRC"),
        ("Confirmation Letter", "Confirmation Letter"),
    ]

    PROCUREMENT_CHOICES = [
        ("NCT", "NCT"),
        ("ICT", "ICT"),
        ("DC", "DC"),
    ]

    tender = forms.ModelChoiceField(
        queryset=Tender.objects.none(),
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            }
        ),
    )

    type_of_letter = forms.ChoiceField(
        choices=LETTER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            }
        ),
    )

    procurement_type = forms.ChoiceField(
        choices=PROCUREMENT_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            }
        ),
    )

    class Meta:
        model = ISODetail
        fields = ["tender", "type_of_letter", "procurement_type"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["tender"].queryset = Tender.objects.filter(
                user=user,
                isodetail__isnull=False,  # Only show tenders without ISO
                # status='Approved'# Only show approved tenders
            )
