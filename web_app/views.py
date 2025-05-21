from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .cassandra_utils import session

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            session.execute("""
                INSERT INTO django_users_detail (username, firstname, lastname, age, password, security_question, security_answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                request.POST['username'],
                request.POST['firstname'],
                request.POST['lastname'],
                int(request.POST['age']),
                request.POST['password'],
                request.POST['security_question'],
                request.POST['security_answer']
            ))
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        except Exception:
            messages.error(request, "Username already exists.")
            return redirect('register')
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        result = session.execute("SELECT * FROM django_users_detail WHERE username=%s", (username,))
        user = result.one()
        if user and user.password == password:
            request.session['username'] = username
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        request.session['recover_user'] = username
        result = session.execute("SELECT security_question FROM django_users_detail WHERE username=%s", (username,))
        row = result.one()
        if row:
            return render(request, 'reset_password.html', {
                'step': 'question',
                'question': row.security_question,
                'step_action': 'security_question'
            })
        else:
            messages.error(request, "Username not found.")
    return render(request, 'reset_password.html', {'step': 'username', 'step_action': 'forgot_password'})

@csrf_exempt
def security_question(request):
    if request.method == 'POST':
        answer = request.POST['answer']
        username = request.session.get('recover_user')
        result = session.execute("SELECT security_answer FROM django_users_detail WHERE username=%s", (username,))
        row = result.one()
        if row and row.security_answer == answer:
            return render(request, 'reset_password.html', {
                'step': 'new_password',
                'step_action': 'reset_password'
            })
        else:
            messages.error(request, "Incorrect answer.")
            return redirect('forgot_password')

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        username = request.session.get('recover_user')
        session.execute("UPDATE django_users_detail SET password=%s WHERE username=%s", (new_password, username))
        messages.success(request, "Password reset successful.")
        return redirect('login')

def dashboard(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'dashboard.html', {'username': request.session['username']})

def logout_view(request):
    request.session.flush()
    return redirect('home')

def delete_user(request):
    username = request.session.get('username')
    session.execute("DELETE FROM django_users_detail WHERE username=%s", (username,))
    request.session.flush()
    messages.success(request, "Account deleted.")
    return redirect('home')