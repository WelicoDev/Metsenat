from django import forms

from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username" , "first_name" , "last_name" , "email" , "password")

    def save(self , commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])

        user.save()

        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'username' , 'first_name' , 'last_name' , 'email')