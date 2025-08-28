from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone

from app1.models import *


# Create your views here.




@login_required
def dashboard(request):
    sections = Section.objects.all()
    context = {'sections': sections}
    return render(request, 'dashboard.html', context)

@login_required
def section_overview(request, section_id):
    section = Section.objects.get(id=section_id)
    lanes = Lane.objects.filter(section=section)
    note = NotePending.objects.filter(lane__in=lanes, is_resolved=False)
    context = {'section': section, 'lanes': lanes, 'note': note}
    return render(request, 'section_overview.html', context)

@login_required
def lane_errors(request, lane_id):
    lane = Lane.objects.get(id=lane_id)
    error_logs = lane.errorlog_set.filter(is_resolved=False)
    if request.method == 'POST':
        selected_ids = request.POST.getlist('errorlog_ids')
        description = request.POST.get('description', '')
        selected_errorlogs = error_logs.filter(id__in=selected_ids)
        if selected_errorlogs.exists():
            repair_log = RepairLog.objects.create(
                lane=lane,
                description=description,
                repaired_by=request.user
            )
            repair_log.error.set(selected_errorlogs)
            # Mark error logs as resolved and set resolved_by
            selected_errorlogs.update(is_resolved=True, resolved_by=request.user)
            return render(request, 'lane_errors.html', {
                'lane': lane,
                'error_logs': error_logs,
                'success': 'Repair log created successfully! Selected errors marked as resolved.'
            })
        else:
            return render(request, 'lane_errors.html', {
                'lane': lane,
                'error_logs': error_logs,
                'error': 'Please select at least one error log.'
            })
    return render(request, 'lane_errors.html', {'lane': lane, 'error_logs': error_logs})

class RepairLogFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date To')
    
    class Meta:
        model = RepairLog
        fields = ['lane', 'date_from', 'date_to']
        widgets = {
            'lane': forms.Select(attrs={'class': 'form-control'}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    

@login_required
def my_repairs(request):
    form = RepairLogFilterForm(request.GET or None)
    repair_logs = RepairLog.objects.filter(repaired_by=request.user).order_by('-created_at')
    if form.is_valid():
        lane = form.cleaned_data.get('lane')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if lane:
            repair_logs = repair_logs.filter(lane=lane)
        if date_from:
            repair_logs = repair_logs.filter(date__date__gte=date_from)
        if date_to:
            repair_logs = repair_logs.filter(date__date__lte=date_to)
    return render(request, 'my_repairs.html', {'repair_logs': repair_logs, 'form': form})

@login_required
def edit_note_pending_app2(request, note_id):
    note_pending = get_object_or_404(NotePending, id=note_id)
    if request.method == 'POST':
        resolving_report = request.POST.get('resolving_report', '').strip()
        if resolving_report:
            note_pending.resolving_report = resolving_report
            note_pending.save()
            if note_pending.is_resolved:
                return redirect('broken_lane_resolves')
            else:
                note_pending.is_resolved = True
                note_pending.resolved_by = request.user
                note_pending.save()
                return redirect('section_overview', section_id=note_pending.lane.section.id)
        else:
            error = 'Please provide a resolving report.'
            return render(request, 'edit_note_pending_app2.html', {'note_pending': note_pending, 'error': error})
    return render(request, 'edit_note_pending_app2.html', {'note_pending': note_pending})

class NotePendingFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane')
    is_resolved = forms.ChoiceField(choices=[('', 'All'), ('True', 'Resolved'), ('False', 'Unresolved')], required=False, label='Status')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date To')

@login_required
def broken_lane_resolves(request):
    form = NotePendingFilterForm(request.GET or None)
    notes = NotePending.objects.all().order_by('-created_at')
    if form.is_valid():
        lane = form.cleaned_data.get('lane')
        is_resolved = form.cleaned_data.get('is_resolved')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if lane:
            notes = notes.filter(lane=lane)
        if is_resolved == 'True':
            notes = notes.filter(is_resolved=True)
        elif is_resolved == 'False':
            notes = notes.filter(is_resolved=False)
        if date_from:
            notes = notes.filter(created_at__date__gte=date_from)
        if date_to:
            notes = notes.filter(created_at__date__lte=date_to)
    return render(request, 'broken_lane_resolves.html', {'notes': notes, 'form': form})

class ErrorLogFilterForm(forms.Form):
    lane = forms.ModelChoiceField(queryset=Lane.objects.all(), required=False, label='Lane')
    error = forms.ModelChoiceField(queryset=Error.objects.all(), required=False, label='Error Type')
    is_resolved = forms.ChoiceField(choices=[('', 'All'), ('True', 'Resolved'), ('False', 'Unresolved')], required=False, label='Status')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date To')

@login_required
def all_error_logs(request):
    form = ErrorLogFilterForm(request.GET or None)
    error_logs = ErrorLog.objects.all().order_by('-created_at')
    if form.is_valid():
        lane = form.cleaned_data.get('lane')
        error = form.cleaned_data.get('error')
        is_resolved = form.cleaned_data.get('is_resolved')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        if lane:
            error_logs = error_logs.filter(lane=lane)
        if error:
            error_logs = error_logs.filter(error=error)
        if is_resolved == 'True':
            error_logs = error_logs.filter(is_resolved=True)
        elif is_resolved == 'False':
            error_logs = error_logs.filter(is_resolved=False)
        if date_from:
            error_logs = error_logs.filter(created_at__date__gte=date_from)
        if date_to:
            error_logs = error_logs.filter(created_at__date__lte=date_to)
    return render(request, 'all_error_logs.html', {'error_logs': error_logs, 'form': form})

@login_required
def all_errors(request):
    errors = Error.objects.all().order_by('number')
    return render(request, 'all_errors.html', {'errors': errors})

class ErrorForm(forms.ModelForm):
    class Meta:
        model = Error
        fields = ['number', 'description']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

@login_required
def add_error(request):
    if request.method == 'POST':
        form = ErrorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_errors')
    else:
        form = ErrorForm()
    return render(request, 'add_error.html', {'form': form})

@login_required
def edit_error(request, error_id):
    error = get_object_or_404(Error, id=error_id)
    if request.method == 'POST':
        form = ErrorForm(request.POST, instance=error)
        if form.is_valid():
            form.save()
            return redirect('all_errors')
    else:
        form = ErrorForm(instance=error)
    return render(request, 'edit_error.html', {'form': form, 'error': error})