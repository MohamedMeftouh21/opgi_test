from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django import template

register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# Create your views here.
@unauthenticated_user

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if Group.objects.filter(user=user, name='service_contentieux').exists():
                return redirect('home')
                
            elif Group.objects.filter(user=user, name='service_recouvrement').exists():
                return redirect('home')
            
            else:
                return redirect('abcd')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'registration/login.html')

def abcd(request):
	            return HttpResponse("Cannot sanitize form data")
def logoutUser(request):
	logout(request)
	return redirect('accounts:login')