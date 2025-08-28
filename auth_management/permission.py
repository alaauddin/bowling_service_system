
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def admin_role(request):
    if request.user.groups.filter(name='Admin').exists():
        return True
    else:
        return False

    
@login_required
def maintenance_role(request):
    print(request.META.get('HTTP_REFERER') and '/auth/login/' in request.META.get('HTTP_REFERER'))
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Maintenance').exists():
        return True
    else:
        return False
    
@login_required
def staff_role(request):
    if request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Staff').exists():
        print( "staff role")
        return True
    else:
        return False
        
        
