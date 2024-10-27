from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm, AddRecordForm, UpdateRecordStatusForm
from .models import Record, UserProfile


def home(request):
	if request.user.is_authenticated:
		try:
			if is_admin(request.user):
				records = Record.objects.all()
				# Get regular users for the assign dropdown
				users = User.objects.filter(userprofile__user_type='regular')
			else:
				records = Record.objects.filter(assigned_to=request.user)
				users = None
			return render(request, 'home.html', {
				'records': records,
				'users': users
			})
		except:
			messages.error(request, "User profile error. Please contact admin.")
			return redirect('logout')
	else:
		return render(request, 'home.html', {'records': []})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			# If this is the first user, make them an admin
			if User.objects.count() == 1:
				user.userprofile.user_type = 'admin'
				user.userprofile.save()
			
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	if request.user.is_authenticated and request.method == "POST":
		if is_admin(request.user):
			form = AddRecordForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "Record Added Successfully!")
			else:
				messages.error(request, "Error Adding Record. Please check the form.")
		else:
			messages.error(request, "You don't have permission to add records.")
	return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def is_admin(user):
	if not user.is_authenticated:
		return False
	try:
		return user.userprofile.user_type == 'admin'
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(
			user=user,
			user_type='admin' if user.is_superuser else 'regular'
		)
		return profile.user_type == 'admin'


@login_required
def update_record_status(request, pk):
	record = Record.objects.get(id=pk)
	
	# Check if user has permission to update this record
	if not is_admin(request.user) and record.assigned_to != request.user:
		messages.error(request, "You don't have permission to update this record.")
		return redirect('home')
	
	if request.method == 'POST':
		form = UpdateRecordStatusForm(request.POST, instance=record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record status updated successfully!")
			return redirect('home')
	else:
		form = UpdateRecordStatusForm(instance=record)
	
	return render(request, 'update_status.html', {'form': form, 'record': record})


@login_required
@user_passes_test(is_admin)
def assign_record(request, pk):
	record = Record.objects.get(id=pk)
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id:
			record.assigned_to_id = user_id
			record.save()
			messages.success(request, "Record assigned successfully!")
		return redirect('home')
	
	regular_users = User.objects.filter(userprofile__user_type='regular')
	return render(request, 'assign_record.html', {
		'record': record,
		'users': regular_users
	})
