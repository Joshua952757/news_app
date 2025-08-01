from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


USER_TYPES =  [("READER", "reader"), ("JOURNALIST", "journalist"),("EDITOR", "editor"),("ADMIN", "admin")]  # Defines choices for user type.


class RegisterForm(UserCreationForm):
    """
    Custom registration form extending Django's UserCreationForm.

    Adds 'bio' (textarea) and 'type' (choice field) to the standard user creation fields.
    These extra fields are used to populate the associated Profile model.
    """
    bio = forms.CharField(widget=forms.Textarea) # Field for user's biography.
    role = forms.ChoiceField(choices=USER_TYPES) # Field for selecting user's role (four options).

    class Meta:
        """
        Meta class defines the model and fields for the form.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'bio', 'role']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username']

class UpdateProfileForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Profile.Role,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['role'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self._original_role = self.instance.role
        else:
            self._original_role = None

    def save(self, commit=True):
        profile = super().save(commit=False)
        new_role = self.cleaned_data.get('role')

        if new_role != self._original_role:
            if new_role == Profile.Role.JOURNALIST:
                profile.sub_journalist.clear()
                profile.sub_publisher.clear()
            elif new_role == Profile.Role.READER:
                if profile.publisher:
                    profile.publisher = None
            elif new_role in [Profile.Role.ADMIN, Profile.Role.EDITOR]:
                profile.sub_journalist.clear()
                profile.sub_publisher.clear()
                if profile.publisher:
                    profile.publisher = None

        if commit:
            profile.save()
        return profile