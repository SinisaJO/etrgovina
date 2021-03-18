from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

def prijava(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('prodavnica')
        else:
            messages.info(request, 'Username or Password is incorect!')

    sadrzaj = {}
    return render(request, 'prijava.html', sadrzaj)     

def registracija(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            #messages.success(request, 'Korisnik ' + user + ' je uspesno kreirao nalog!')

            return redirect('prijava')

    sadrzaj = {'form': form}
    return render(request, 'registracija.html', sadrzaj) 

def odjava(request):
    logout(request)
    return redirect('prijava')