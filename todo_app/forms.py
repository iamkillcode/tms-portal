from django import forms
from .models import ToDoList, ToDoItem, ToDoComment, ToDoAttachment, ToDoTag
from tender_app.models import TaskCategory


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }


class ToDoItemForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False, 
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
    
    reminder_date = forms.DateTimeField(
        required=False, 
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
    
    recurrence_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = ToDoItem
        fields = [
            'title', 'description', 'todo_list', 'category', 'priority', 
            'status', 'progress', 'due_date', 'recurrence', 
            'recurrence_end_date', 'reminder_date', 'is_flagged', 'is_pinned'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'todo_list': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'max': 100,
                'type': 'range'
            }),
            'recurrence': forms.Select(attrs={'class': 'form-select'}),
            'is_flagged': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter todo lists by user
        self.fields['todo_list'].queryset = ToDoList.objects.filter(user=user)
        # Filter categories by user or those that are global (no user)
        self.fields['category'].queryset = TaskCategory.objects.filter(
            user=user
        )


class ToDoCommentForm(forms.ModelForm):
    class Meta:
        model = ToDoComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ToDoAttachmentForm(forms.ModelForm):
    class Meta:
        model = ToDoAttachment
        fields = ['file', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ToDoTagForm(forms.ModelForm):
    class Meta:
        model = ToDoTag
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }
