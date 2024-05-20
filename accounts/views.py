from django.shortcuts import render, redirect
# from .forms import RegistrationForm
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# from crispy_forms.helper import FormHelper
# Create your views here.
#verification email
from django.contrib.auth.decorators import login_required


def register(request):

	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password == password2:
			if User.objects.filter(email=email).exists():
				messages.info(request, 'Email Taken')
				return redirect('signup')
			elif User.objects.filter(username=username).exists():
				messages.info(request, 'Username Taken')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username, email=email, password=password)
				user.save()

				#log user in and direct to settings page
				user_login = auth.authenticate(username=username, password=password)
				auth.login(request, user_login)


				#create a profile object for the new user
				user_model = User.objects.get(username=username)
				new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
				new_profile.save()
				return redirect('home')
		else:
			messages.info(request, 'Password Not Matching')
			return redirect('register')
	else:
		return render(request, 'accounts/register.html')

# def login(request):
# 	if request.method == 'POST':
# 		email = request.POST['email']
# 		password = request.POST['password']

# 		user = authenticate(request, email=email, password=password)

# 		if user is not None:
# 			login(request, user)
# 			return redirect('home')
# 		else:
# 			messages.error(request, 'Invalid login credentials')
# 			return redirect('login')
# 	else:
# 		return render(request, 'accounts/login.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Credentials Invalid')
			return redirect('login')
	else:
		return render(request, 'accounts/login.html')

# def  register(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			email = form.cleaned_data['email']
# 			password = form.cleaned_data['password']
# 			user = authenticate(email=email, password=password)
# 			login(request, user)
# 			messages.success(request, ("Registration Successful"))
# 			return redirect('home')

# 	else:
# 		form = UserCreationForm()
# 	return render(request, 'accounts/register.html',{'form': form,})

# def login(request):
# 	if request.method == 'POST':
# 		if form.is_valid():
# 			email = form.cleaned_data['email']
# 			password = form.cleaned_data['password']
# 			user = authenticate(request, email=email, password=password)
# 			if user is not None:
# 				login(request, user)
# 				return redirect('home')
# 		else:
# 			messages.success(request, ("There Was An Error"))
# 			return redirect('login')
# 	return render(request, 'accounts/login.html')



@login_required(login_url='login')
def logout(request):
	auth.logout(request)
	messages.success(request, "you are logged out")
	return redirect('login')

@login_required(login_url='login')
def dashboard(request):
	return render(request, 'accounts/dashboard.html')
