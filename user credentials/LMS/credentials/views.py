from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Tutor, UserSubscription, UserProfile
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


def homepage(request):
    return render(request, "pages/homepage.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():  
            messages.error(request, "Username already exists!! Please try another username")
            return redirect('homepage')

        if User.objects.filter(email=email).exists(): 
            messages.error(request, "Email already registered to another account!!")
            return redirect('homepage')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "Password does not match! ")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha numeric!")
            return redirect('homepage')  

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        
        UserProfile.objects.create(user=myuser)

        messages.success(request, "Your Account has been successfully created.")
        return redirect('signin')

    return render(request, "pages/signup.html")


def subription(request):
    user = request.user
    if UserSubscription.objects.filter(user=user).exists():
        return render(request,'subcription_already_exists.html')
    subscription_start_date = timezone.now()
    subscription_end_date = subscription_start_date + timedelta(weeks=1)
    
    subscription = UserSubscription.objects.create(
        user=user,
        subscription_start_date=subscription_start_date,
        subscription_end_date=subscription_end_date
    
    )
    return render(render, 'subscription_success.html', {'subscription': subscription})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/homepage.html", {'fname': fname})
        else:
            messages.error(request, "Wrong password or username!")
            return redirect('homepage')

    return render(request, "pages/signin.html")


def user_profile(request):
    if request.method == 'POST':
        user = request.user
        tutor_details = Tutor.objects.filter(user=user).first()
        
        return render(request, 'profile.html', {'user': user, 'tutor_details': tutor_details})
    
def signout(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')


def UserSubscription(request):
    UserSubscription = UserSubscription.objects.all()
    user_profile = Tutor.objects.filter(user=request.user).first()
    
    
    if request.method == 'POST':
        selected_plan_id = request.POST.get('selected_plan')
        selected_plan = get_object_or_404(UserSubscription, pk=selected_plan_id)
        
        user_profile = request.user.userprofile
        user_profile.selected_plan = selected_plan
        user_profile.save()
        
        messages.success(request, 'Plan successfully selected.')
        return redirect('home') 
        
    else:
        messages.warning(request, 'You need to log in to choode a plan')      
    
        return render(request, 'credentials/choose_plan.html')


