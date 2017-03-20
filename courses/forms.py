from django import forms


class AssignmentSubmissionForm(forms.Form):
    link = forms.URLField(max_length=100, required=True)
    file = forms.FileField(required=False)
    notes = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['link'].widget.attrs = {
            'class': 'form-control'
        }
        # self.fields['file'].widget.attrs = {
        #     'class': 'form-control'
        # }
        self.fields['notes'].widget.attrs = {
            'class': 'form-control'
        }
