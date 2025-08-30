from django import forms
from .models import ErrorLog, Error, NotePending, DailyCheckList

class ErrorLogForm(forms.ModelForm):
    error = forms.ModelChoiceField(queryset=Error.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    class Meta:
        model = ErrorLog
        fields = ['error', 'notes']

class NotePendingForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), label='Note')
    class Meta:
        model = NotePending
        fields = ['note']

class EditNotePendingForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), label='Edit Note')
    class Meta:
        model = NotePending
        fields = ['note']

class DailyCheckListForm(forms.ModelForm):
    electrical_check = forms.BooleanField(required=False, label='فحص كهربائي')
    is_cleaned = forms.BooleanField(required=False, label='تم التنظيف')
    oprated_smoothly = forms.BooleanField(required=False, label='يعمل بسلاسة')
    no_defects = forms.BooleanField(required=False, label='لا يوجد عيوب')
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False, label='ملاحظات')
    class Meta:
        model = DailyCheckList
        fields = ['electrical_check', 'is_cleaned', 'oprated_smoothly', 'no_defects', 'notes']

class EditDailyCheckListForm(forms.ModelForm):
    electrical_check = forms.BooleanField(required=False, label='فحص كهربائي')
    is_cleaned = forms.BooleanField(required=False, label='تم التنظيف')
    oprated_smoothly = forms.BooleanField(required=False, label='يعمل بسلاسة')
    no_defects = forms.BooleanField(required=False, label='لا يوجد عيوب')
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False, label='ملاحظات')
    class Meta:
        model = DailyCheckList
        fields = ['electrical_check', 'is_cleaned', 'oprated_smoothly', 'no_defects', 'notes']
