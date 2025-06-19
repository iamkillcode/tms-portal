from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import (UserProfile, TenderItem, VendorBid, FrameworkAgreement, 
                    Vendor, Chemical, ChemicalSpecification, Task, TaskCategory, TaskComment, Department, Tender)

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

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority', 'tender', 'vendor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TaskCategoryForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'}),
        initial='#007bff'
    )
    
    class Meta:
        model = TaskCategory
        fields = ['name', 'color']

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'contact_person', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company/Vendor Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Contact Person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email Address'}),
        }

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'avatar', 'bio', 'phone', 'department']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            
    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        # Update the associated User model
        if profile.user:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            if commit:
                profile.user.save()
                profile.save()
        return profile

class TenderUpdateForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(),
        label="Vendor/Consultant Name:",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tender
        fields = [
            # ...existing fields...
            'vendor',
            # ...existing fields...
        ]
