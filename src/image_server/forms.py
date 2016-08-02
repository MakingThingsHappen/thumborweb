from django import forms


class FileNameForm(forms.Form):
    filename = forms.CharField(max_length=255, min_length=1)
