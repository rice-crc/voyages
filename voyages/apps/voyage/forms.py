from django import forms

class UploadFileForm(forms.Form):
    '''
    Form to uploading files in download section
    '''
    downloadfile = forms.FileField(label='Select your file')

