from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Section)
admin.site.register(Lane)
admin.site.register(Error)
admin.site.register(NotePending)
admin.site.register(DailyCheckList)

