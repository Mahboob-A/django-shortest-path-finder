from django import forms
from .models import Places

class ShortestPathForm(forms.Form): 
        source_place = forms.ModelChoiceField(queryset=Places.objects.all(), widget=forms.Select(attrs={'class' : 'form-select col-6'}))  # the attrs is bootstrap dropdown class 
        destination_place = forms.ModelChoiceField(queryset=Places.objects.all(), widget=forms.Select(attrs={'class' : 'form-select col-6'}))
        
        def clean(self):  # overririding the clean method 
                cleaned_data = super().clean()
                
                source_place = cleaned_data.get('source_place')
                destination_place = cleaned_data.get('destination_place')
                
                if source_place == destination_place: 
                        raise forms.ValidationError('Source and Destination can not be same')
                
                return cleaned_data
