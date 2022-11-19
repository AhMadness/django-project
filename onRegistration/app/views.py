from django.shortcuts import render
from app.forms import UserForm, ProfileForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user   # For one to one
            
            if 'profpic' in request.FILES:
                profile.profpic = request.FILES['profpic']
                
            profile.save()
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    
    return render(request, 'app/registration.html',
                  {'user_form': user_form,
                   "profile_form": profile_form,
                   "registered": registered})
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            
            else:
                return HttpResponse("Account Not Active!")
        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid Login Details!")
    else:
        return render(request, 'app/login.html', {})
            