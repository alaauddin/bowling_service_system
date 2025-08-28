from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import ErrorLog, Lane, Section, Error, NotePending
from .forms import ErrorLogForm
from auth_management.permission import  staff_role
from django.contrib import messages


from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')
    sections = Section.objects.all()
    context = {'sections': sections}
    return render(request, 'home.html', context)

@login_required
def section_detail(request, section_id):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    lane = Lane.objects.filter(section_id=section_id)
    section = get_object_or_404(Section, id=section_id)
    section_today_checklist = section.get_today_checklist(request.user)
    context = {'lane': lane, 'section_today_checklist': section_today_checklist}
    return render(request, 'section_detail.html', context)

@login_required
def lane_detail(request, lane_id):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    error_logs = ErrorLog.objects.filter(lane_id=lane_id)
    context = {'error_logs': error_logs}
    return render(request, 'lane_detail.html', context)

@login_required
def add_errorlog(request, lane_id):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    lane = get_object_or_404(Lane, id=lane_id)
    if request.method == 'POST':
        form = ErrorLogForm(request.POST)
        if form.is_valid():
            errorlog = form.save(commit=False)
            errorlog.lane = lane
            errorlog.created_by = request.user
            errorlog.save()
            return redirect('section_detail', lane.section.id)
    else:
        form = ErrorLogForm()
    return render(request, 'add_errorlog.html', {'form': form, 'lane': lane})

@login_required
def add_note_pending(request, lane_id):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    lane = get_object_or_404(Lane, id=lane_id)
    if lane.has_none_resolved_notes():
        return render(request, 'add_note_pending.html', {
            'error': 'There is already a pending unresolved note for this lane.',
            'lane': lane
        })
    if request.method == 'POST':
        from .forms import NotePendingForm
        form = NotePendingForm(request.POST)
        if form.is_valid():
            note_pending = form.save(commit=False)
            note_pending.lane = lane
            note_pending.created_by = request.user
            note_pending.save()
            return redirect('section_detail', section_id=lane.section.id)
    else:
        from .forms import NotePendingForm
        form = NotePendingForm()
    return render(request, 'add_note_pending.html', {'form': form, 'lane': lane})

@login_required
def edit_note_pending(request, note_id):
    from .forms import EditNotePendingForm
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    note_pending = get_object_or_404(NotePending, id=note_id)
    if note_pending.created_by != request.user:
        messages.error(request, "You can only edit notes you have created.")
        return redirect('section_detail', section_id=note_pending.lane.section.id)
    if request.method == 'POST':
        if note_pending.created_by != request.user:
            messages.error(request, "You can only edit notes you have created.")
            return redirect('section_detail', section_id=note_pending.lane.section.id)
        form = EditNotePendingForm(request.POST, instance=note_pending)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect('section_detail', section_id=note_pending.lane.section.id)
    else:
        form = EditNotePendingForm(instance=note_pending)
    return render(request, 'edit_note_pending.html', {'form': form, 'note_pending': note_pending})

@login_required
def add_daily_checklist(request, section_id):
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    section = get_object_or_404(Section, id=section_id)
    from .forms import DailyCheckListForm
    from .models import DailyCheckList
    from django.utils import timezone
    today = timezone.now().date()
    already_exists = DailyCheckList.objects.filter(section=section, date=today, created_by=request.user).exists()
    if already_exists:
        return render(request, 'add_daily_checklist.html', {
            'error': 'You have already submitted a checklist for this section today.',
            'section': section
        })
    if request.method == 'POST':
        form = DailyCheckListForm(request.POST)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.section = section
            checklist.date = today
            checklist.created_by = request.user
            checklist.save()
            return redirect('section_detail', section_id=section.id)
    else:
        form = DailyCheckListForm()
    return render(request, 'add_daily_checklist.html', {'form': form, 'section': section})

@login_required
def edit_daily_checklist(request, checklist_id):
    from .forms import EditDailyCheckListForm
    from .models import DailyCheckList
    if not staff_role(request):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home_genaric')(request)
    checklist = get_object_or_404(DailyCheckList, id=checklist_id)
    if request.method == 'POST':
        form = EditDailyCheckListForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect('section_detail', section_id=checklist.section.id)
    else:
        form = EditDailyCheckListForm(instance=checklist)
    return render(request, 'edit_daily_checklist.html', {'form': form, 'checklist': checklist})


