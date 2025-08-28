from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


from .permission import admin_role, maintenance_role, staff_role
@login_required
def home_genaric(request):
    if admin_role(request):
        return render(request, 'home_genaric.html')
    elif maintenance_role(request):
        return redirect('dashboard')
    elif staff_role(request):
        return redirect('home')
    else:
        return render(request, 'home_genaric.html')
        
        

