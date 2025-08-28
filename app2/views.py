from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone

from app1.models import *

from auth_management.permission import admin_role, maintenance_role

# Create your views here.




@login_required
def dashboard(request):
    if not maintenance_role(request):
        return redirect('home_genaric')
    sections = Section.objects.all()
    context = {'sections': sections}
    return render(request, 'dashboard.html', context)

@login_required
def section_overview(request, section_id):
    if not maintenance_role(request):
        return redirect('home_genaric')
    section = Section.objects.get(id=section_id)
    lanes = Lane.objects.filter(section=section)
    note = NotePending.objects.filter(lane__in=lanes, is_resolved=False)
    context = {'section': section, 'lanes': lanes, 'note': note}
    return render(request, 'section_overview.html', context)

@login_required
def lane_errors(request, lane_id):
    if not maintenance_role(request):
        return redirect('home_genaric')
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



@login_required
def my_repairs(request):
    from .forms import RepairLogFilterForm
    if not maintenance_role(request):
        return redirect('home_genaric')
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
    if not maintenance_role(request):
        return redirect('home_genaric')
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


@login_required
def broken_lane_resolves(request):
    from .forms import NotePendingFilterForm
    if not maintenance_role(request):
        return redirect('home_genaric')
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


@login_required
def all_error_logs(request):
    from .forms import ErrorLogFilterForm
    if not maintenance_role(request):
        return redirect('home_genaric')
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
    if not admin_role(request):
        return redirect('home_genaric')
    errors = Error.objects.all().order_by('number')
    return render(request, 'all_errors.html', {'errors': errors})



@login_required
def add_error(request):
    from .forms import ErrorForm
    if not admin_role(request):
        return redirect('home_genaric')
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
    from .forms import ErrorForm
    if not admin_role(request):
        return redirect('home_genaric')
    else:
        error = get_object_or_404(Error, id=error_id)
        if request.method == 'POST':
            form = ErrorForm(request.POST, instance=error)
            if form.is_valid():
                form.save()
                return redirect('all_errors')
        else:
            form = ErrorForm(instance=error)
        return render(request, 'edit_error.html', {'form': form, 'error': error})