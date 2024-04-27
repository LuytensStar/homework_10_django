from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterForm,LoginForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def singupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quoteapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')

        else:
            return render(request, 'users/signup.html', context={'form':form})

    return render(request, 'users/signup.html', context={'form': RegisterForm()})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='quoteapp:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])

        if user is None:
            messages.error(request,"Password or username doesnot mathc")
            return redirect(to='users:login')

        login(request,user)
        return redirect(to='quoteapp:main')

    return render(request,'users/login.html', context= {'form': LoginForm()})
# Create your views here.

@login_required
def logoutuser(request):
    login(request)
    return redirect(to='qouteapp:main')

@login_required
def profile(request):
    return render(request,'users/profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})
