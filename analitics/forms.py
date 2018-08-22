from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['docfile'].widget.attrs.update({'class': 'norm_font border btn-big'})
        self.fields['docfile'].widget.attrs.update({'accept': '.txt'})