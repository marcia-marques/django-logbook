from django import forms


def DataRaw24hFormFunction(date_choices):

    class DataRaw24hForm(forms.Form):
        days = forms.ChoiceField(widget=forms.Select(
            attrs={'class': 'form-select form-select-sm'}),
            choices=date_choices)

    return DataRaw24hForm
