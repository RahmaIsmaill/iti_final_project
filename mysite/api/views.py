from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProjectForm
from .models import User, Project
from django.contrib.auth.decorators import login_required
from datetime import datetime

# ------------------ Authentication ------------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect("login")

            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {user.first_name}!")
                return redirect("project_list")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# ------------------ Project Management ------------------

@login_required
def project_list(request):
    projects = Project.objects.all()


    # بحث حسب التاريخ (اختياري)
    search_date = request.GET.get("date")
    if search_date:
        try:
            date_obj = datetime.strptime(search_date, "%Y-%m-%d").date()
            projects = projects.filter(start_date__lte=date_obj, end_date__gte=date_obj)
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")

    return render(request, "project_list.html", {"projects": projects})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, "Project created successfully!")
            return redirect("project_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm()
    return render(request, "project_form.html", {"form": form, "title": "Create Project"})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            edited_project = form.save(commit=False)
            edited_project.save()
            messages.success(request, "Project updated successfully!")
            return redirect("project_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProjectForm(instance=project)
    return render(request, "project_form.html", {"form": form, "title": "Edit Project"})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("project_list")
    return render(request, "project_confirm_delete.html", {"project": project})

@login_required
def project_profile_view(request):
    return render(request, "profile.html")