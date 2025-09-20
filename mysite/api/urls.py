from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    project_list,
    project_create,
    project_edit,
    project_delete,
    project_profile_view
)

urlpatterns = [
    # Authentication
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Project Management
    path("projects/", project_list, name="project_list"),
    path("projects/create/", project_create, name="project_create"),
    path("projects/<int:pk>/edit/", project_edit, name="project_edit"),
    path("projects/<int:pk>/delete/", project_delete, name="project_delete"),
     path("profile/",  project_profile_view, name="profile"),
]
