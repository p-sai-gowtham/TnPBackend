from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json


def signin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid input"}, status=400)

        # Check if the user exists
        if not User.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "User doesn't exist. Please sign up"}, status=404
            )

        user = User.objects.get(email=email)
        authenticated_user = authenticate(request, username=email, password=password)

        if authenticated_user is not None:
            # Check the password using check_password
            if check_password(password, authenticated_user.password):
                login(request, authenticated_user)
                # Manually serialize only the required fields
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_student": user.is_student,
                    "reg_no": user.reg_no,
                }
                return JsonResponse({"message": "Login Successful", "user": user_data}, safe=False, status=200)
            else:
                return JsonResponse({"message": "Invalid password"}, status=401)
        else:
            return JsonResponse({"message": "Authentication failed"}, status=401)



def logout_view(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('user:login')

def add_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists!')
            return redirect('app:admin') 
        password = request.POST.get('password') 
        dashboard = request.POST.get('dashboard') == 'on'
        admin = request.POST.get('admin') == 'on'
        hashed_password = make_password(password) 
        user = User.objects.create(
            username=email,
            email=email,
            password= hashed_password,
            dashboard=dashboard,
            admin=admin,
        )
        messages.success(request, 'User added successfully!')
        return redirect('app:admin')  # Redirect to the appropriate URL

    return render(request, 'your_template.html')

def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        print(request.POST)
        user.email = request.POST.get('email')
        if request.POST.get('password'):
            user.password = make_password(request.POST.get('password'))
        user.save()

        messages.success(request, 'User updated successfully!')
        return redirect('app:admin')  # Redirect to the appropriate URL

    context = {'user': user}
    return redirect('app:adminview')

def remove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_superuser:
        messages.error(request, 'SuperUser cannot be deleted!')
        return redirect('app:admin')
    user.delete()

    messages.success(request, 'User deleted successfully!')
    return redirect('app:admin')

