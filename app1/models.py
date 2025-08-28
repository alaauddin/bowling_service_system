from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_today_checklist(self, user):
        from django.utils import timezone
        today = timezone.now().date()
        return self.dailychecklist_set.filter(date=today, created_by=user).first()
    
class Lane(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lane {self.number} in {self.section.name}"
    
    def has_none_resolved_notes(self):
        return self.notepending_set.filter(is_resolved=False).exists()
    
    def get_none_resolved_notes(self):
        return self.notepending_set.filter(is_resolved=False)
    
    def get_error_logs_count(self):
        return self.errorlog_set.filter(is_resolved=False).count()
    
class DailyCheckList(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    electrical_check = models.BooleanField(default=False)
    is_cleaned = models.BooleanField(default=False)
    oprated_smoothly = models.BooleanField(default=False)
    no_defects = models.BooleanField(default=False)    
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checklist for {self.section} on {self.date}"
    
class Error(models.Model):
    number = models.CharField(max_length=10)
    description = models.CharField(max_length=100)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Error {self.number}: {self.description}"
    
class ErrorLog(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    error = models.ForeignKey(Error, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='errors_resolved', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='error_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ErrorLog for {self.lane} - {self.error} on {self.date} at {self.time}"
    
class RepairLog(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    error = models.ManyToManyField(ErrorLog)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    repaired_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repairs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"RepairLog for {self.lane} on {self.date}"
    
    
class NotePending(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    note = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_resolved', blank=True, null=True)
    resolving_report = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"NotePending for {self.lane} - Resolved: {self.is_resolved}"
