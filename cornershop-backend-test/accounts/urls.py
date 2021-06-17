from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.IndexView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("client/", views.ClientView.as_view(), name="client"),
    path(
        "client/delete/<int:pk>/",
        views.DeleteClientView.as_view(),
        name="delete_client",
    ),
    path("client/edit/<int:pk>/", views.EditClientView.as_view(), name="edit_client"),
]
