from django import forms
from .models import EducationalPublication

class PublicationForm(forms.ModelForm):

    def clean_title(self):
        return self.cleaned_data['title'].strip()
    def clean_link(self):
    
        link = self.cleaned_data['link'].strip()

        if "dailymotion.com/video/" not in link and "dai.ly/" not in link:
            raise forms.ValidationError("Somente links do Dailymotion são permitidos.")

        return link
    
    def clean_description(self):
        return self.cleaned_data['description'].strip()

    class Meta:
        model = EducationalPublication
        fields = ['title', 'description', 'link']