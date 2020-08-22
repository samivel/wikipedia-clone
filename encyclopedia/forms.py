from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title')
    body = forms.CharField(widget=forms.Textarea(), label='Body')
    