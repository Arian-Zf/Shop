from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'address','is_active', 'is_staff')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A user with that phone number already exists.")
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError("A user with that phone number already exists.")

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with that phone number already exists.")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
    
        if not phone.startswith('09'):
            raise forms.ValidationError("Phone number must start with '09'.")

        if len(phone) != 11:
            raise forms.ValidationError("Phone number must be exactly 11 digits long.")
        
        return phone

class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'address','is_active', 'is_staff')