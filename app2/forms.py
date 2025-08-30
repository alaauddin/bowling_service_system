

from django import forms
from app1.models import Error, Lane,  RepairLog
from django.contrib.auth.models import User

class ErrorForm(forms.ModelForm):
    class Meta:
        model = Error
        fields = ['number', 'description']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
class ErrorLogFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane', widget=forms.Select(attrs={'class': 'form-control'}))
    error = forms.ModelChoiceField(queryset=Error.objects.all(), required=False, label='Error Type', widget=forms.Select(attrs={'class': 'form-control'}))
    is_resolved = forms.ChoiceField(choices=[('', 'All'), ('True', 'Resolved'), ('False', 'Unresolved')], required=False, label='Status', widget=forms.Select(attrs={'class': 'form-control'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date To')
    created_by = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Created By',  widget=forms.Select(attrs={'class': 'form-control'}))
    



class NotePendingFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane', widget=forms.Select(attrs={'class': 'form-control'}))
    is_resolved = forms.ChoiceField(choices=[('', 'All'), ('True', 'Resolved'), ('False', 'Unresolved')], required=False, label='Status', widget=forms.Select(attrs={'class': 'form-control'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date To')



class RepairLogFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane', widget=forms.Select(attrs={'class': 'form-control'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date To')
    
    class Meta:
        model = RepairLog
        fields = ['lane', 'date_from', 'date_to']
        widgets = {
            'lane': forms.Select(attrs={'class': 'form-control'}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    
    
class DailyCheckListFormFilter(forms.Form):
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date To')
    created_by = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Created By',  widget=forms.Select(attrs={'class': 'form-control'}))
    
