from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, TenderItem, VendorBid, FrameworkAgreement, Vendor

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, full_name=self.cleaned_data['full_name'])
        return user

class TenderItemForm(forms.ModelForm):
    class Meta:
        model = TenderItem
        fields = ['item_name', 'description', 'quantity', 'unit_of_measure', 
                 'brand', 'manufacturer', 'specifications']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

class VendorBidForm(forms.ModelForm):
    class Meta:
        model = VendorBid
        fields = ['vendor', 'unit_price', 'currency', 'technical_score', 
                 'financial_score', 'remarks', 'is_winner']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class FrameworkAgreementForm(forms.ModelForm):
    class Meta:
        model = FrameworkAgreement
        fields = ['vendor', 'start_date', 'end_date', 'agreement_number', 
                 'status', 'terms_conditions']
        widgets = {
            'terms_conditions': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
