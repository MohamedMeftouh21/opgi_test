from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

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
                return redirect('chat:home')
            elif Group.objects.filter(user=user, name='service_recouvrement').exists():
                return redirect('abcd')
            
            else:
                return redirect('abcd')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'accounts/login.html')

def abcd(request):
	            return HttpResponse("Cannot sanitize form data")
def logoutUser(request):
	logout(request)
	return redirect('login')