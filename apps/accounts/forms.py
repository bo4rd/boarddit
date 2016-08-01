from django import forms

class ProfileChangeForm(forms.Form):
    email = forms.EmailField(label='E-mail:')
