from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm









"""

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
"""

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            #return redirect('home')
            return HttpResponse("xxx")
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})
    #return HttpResponse("hhh")

"""
#sign up function
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #to check validation for this form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #return redirect('home')
            return HttpResponse("hh")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    #return HttpResponse("fffff")
"""

    #login function
