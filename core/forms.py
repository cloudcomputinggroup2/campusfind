from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Item

class ItemForm(forms.ModelForm):
    """
    Form for reporting a Lost or Found item with validation for images and required fields.
    """
    class Meta:
        model = Item
        fields = [
            'title',
            'category',
            'status',
            'location',
            'date_event',
            'description',
            'contact',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Blue Dell Inspiron Laptop with campus sticker',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Science Library, 2nd floor silent reading zone',
                'list': 'location-presets',
                'required': True,
            }),
            'date_event': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed identifiers: color, brand, stickers, scratches, contents inside, etc.',
                'required': True,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Phone: +1 555-0199 or email: student@campus.edu or Campus Security Office',
                'required': True,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'item-image-input',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check maximum file size (5 MB = 5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Image file size must not exceed 5MB.")
            
            # Check allowed extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Allowed image formats are JPG, JPEG, PNG, WEBP, and GIF.")
        return image


class UserRegistrationForm(UserCreationForm):
    """
    Registration form with email, full name, and username requirements.
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@campus.edu'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Campus Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create Password (min 6 chars)'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating basic profile info."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
