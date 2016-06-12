from django import forms

THREAD_TITLE_MIN = 3
THREAD_TITLE_MAX = 100
THREAD_TEXT_MAX = 1024

class ThreadSubmitForm(forms.Form):
    title = forms.CharField(max_length=THREAD_TITLE_MAX, min_length=THREAD_TITLE_MIN, widget=forms.TextInput(attrs={'class': 'form-control'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    text = forms.CharField(max_length=THREAD_TEXT_MAX, widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
