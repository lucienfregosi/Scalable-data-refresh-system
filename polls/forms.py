from django import forms

class NameForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    latitude = forms.FloatField(label='latitude')
    longitude = forms.FloatField(label='longitude')
    accuracy = forms.FloatField(label='accuracy')
