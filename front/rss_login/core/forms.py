from django import forms


class SomeForm(forms.Form):
    some_field = forms.DateTimeField()
