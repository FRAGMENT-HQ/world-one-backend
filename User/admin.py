from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.admin import UserAdmin

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_no', 'email', 'password', 'city' ,'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field."""
  

    class Meta:
        model = User
        fields = ('phone_no', 'email', 'password', 'city' ,'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     return self.initial["password"]

    def save(self, commit=True):
        # Save the user with a hashed password if it's being changed
        user = super().save(commit=False)
        print(self.cleaned_data  )
        # password = self.cleaned_data.get("password")
        # if password:
        #     print(password)
        #     user.set_password(password)
        if commit:
            user.save()
        return user

@admin.register(User)
class userAdmin( admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email','first_name','last_name','phone_no']

# class userAdmin(UserAdmin):
#     ordering = ('email',)
#     list_display = ['email','first_name','last_name','phone_no']
#     search_fields = ('email','first_name','last_name','phone_no')
#     readonly_fields = ('date_joined', 'last_login')
#     exclude = ('username',)
#     pass

# admin.site.register(User, userAdmin)