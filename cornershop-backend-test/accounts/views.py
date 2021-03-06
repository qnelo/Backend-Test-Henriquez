from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, View

from .forms import ClientForm
from .models import Client


class ClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Obtain all clients

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with all clients
        """
        clients = Client.objects.all()
        add_client = ClientForm()
        return render(
            request, "account/client.html", {"clients": clients, "form": add_client}
        )

    def post(self, request, *args, **kwargs):
        """Create a new Client

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to client list
        """
        add_client = ClientForm(request.POST)
        if add_client.is_valid():
            add_client.save()
            return redirect("client")


class DeleteClientView(LoginRequiredMixin, DeleteView):

    model = Client
    success_url = reverse_lazy("client")


class EditClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Obtain a client

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with a client
        """
        client = Client.objects.get(pk=kwargs["pk"])
        add_client = ClientForm(instance=client)
        return render(request, "account/edit_clients.html", {"form": add_client})

    def post(self, request, *args, **kwargs):
        """Modify a Client

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to client list
        """
        client = Client.objects.get(pk=kwargs["pk"])
        edited_client = ClientForm(request.POST, instance=client)
        if edited_client.is_valid():
            edited_client.save()
            return redirect("client")


class IndexView(View):
    def get(self, request, *args, **kwargs):
        """Login site

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with login site
        """
        form = AuthenticationForm()
        return render(
            request=request, template_name="login/index.html", context={"form": form}
        )

    def post(self, request, *args, **kwargs):
        """Login site

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to a main menu
        """
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

        form = AuthenticationForm()
        return render(
            request=request, template_name="login/index.html", context={"form": form}
        )


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        """Logout site

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with login site
        """
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect("login")
