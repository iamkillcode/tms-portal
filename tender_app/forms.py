from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (UserProfile, TenderItem, VendorBid, FrameworkAgreement, 
                    Vendor, Chemical, ChemicalSpecification)

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

class ChemicalImportForm(forms.Form):
    """Form for importing chemical data from Excel files."""
    excel_file = forms.FileField(
        label='Select Excel File',
        help_text='Upload an Excel file containing chemical data. File must be .xlsx format.'
    )
    tender_item = forms.ModelChoiceField(
        queryset=TenderItem.objects.all(),
        label='Select Tender Item',
        help_text='Choose the tender item these chemicals belong to.'
    )

    def clean_excel_file(self):
        file = self.cleaned_data['excel_file']
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('Only Excel files (.xlsx) are allowed.')
        return file

class ChemicalForm(forms.ModelForm):
    """Form for creating/editing individual chemical records."""
    class Meta:
        model = Chemical
        fields = ['chemical_name', 'lot_number', 'formula', 'grade', 
                 'package_size', 'quantity', 'tender_item']
        widgets = {
            'chemical_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'formula': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'package_size': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ChemicalSpecificationForm(forms.ModelForm):
    """Form for adding/editing chemical specifications."""
    class Meta:
        model = ChemicalSpecification
        fields = ['spec_type', 'value', 'unit', 'notes']
        widgets = {
            'spec_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
