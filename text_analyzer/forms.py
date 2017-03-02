from django import forms


class WordForm(forms.Form):
    sentense = forms.CharField(widget=forms.Textarea, label="")



