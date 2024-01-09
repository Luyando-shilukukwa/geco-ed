from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Plan, Tutor


def get_tutor_details(user):
    return Tutor.objects.filter(user=user).first()

@login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            tutor_details = Tutor.objects.filter(user=user).first()
            return redirect('home', tutor_details= tutor_details)
        else:
            messages.error(redirect, 'Invalid username or password!!.')

    return render(request, 'credentials/login.html')

def user_create_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'credentials/create_account.html')


def user_profile(request):
    if request.method == 'POST':
        user = request.user
        tutor_details = Tutor.objects.filter(user=user).first()
        
        return render(request, 'profile.html', {'user': user, 'tutor_details': tutor_details})
    
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')


def choose_plan(request):
    plans = Plan.objects.all()
    tutor_details = Tutor.objects.filter(user=request.user).first()
    
    
    if request.method == 'POST':
        selected_plan_id = request.POST.get('selected_plan')
        selected_plan = get_object_or_404(Plan, pk=selected_plan_id)
        
        user_profile = request.user.userprofile
        user_profile.selected_plan = selected_plan
        user_profile.save()
        
        messages.success(request, 'Plan successfully selected.')
        return redirect('home') 
        
    else:
        messages.warning(request, 'You need to log in to choode a plan')      
    
        return render(request, 'credentials/choose_plan.html')


