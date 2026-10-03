from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            form.save()
            
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, f"Welcome {first_name}, registration successful")
            return redirect('users:login')
        
    return render(request, 'users/register.html', {'form': form})


def logOut(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')