from django import forms


class IndexForm(forms.Form):
    origin = forms.URLField(label='Url', required=True)
    type = forms.ChoiceField(choices=(('Simple', 'simple'), ('Extra', 'extra')),
                             label='Type for your shortcut')
    error = None
    short = None
