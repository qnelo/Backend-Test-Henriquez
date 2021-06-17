import uuid
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, View

import pytz

from .forms import MenuForm, OrderForm, PlateForm
from .models import Menu, Order, Plate


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        """Obtain all menus

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with all menus
        """
        menu_list = Menu.objects.all()[:15]
        add_menu = MenuForm()
        return render(
            request, "kitchen/index.html", {"menu_list": menu_list, "form": add_menu}
        )

    def post(self, request):
        """Create a new Menu

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to menu list
        """
        add_menu = MenuForm(request.POST)
        if add_menu.is_valid():
            add_menu.save()
            return redirect("index")

        menu_list = Menu.objects.all()[:15]
        return render(
            request, "kitchen/index.html", {"menu_list": menu_list, "form": add_menu}
        )


class DailyMenuView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Obtain a Menu

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with a menu
        """

        try:
            menu = get_object_or_404(Menu, date=kwargs["date"])
            orders = Order.objects.filter(menu=menu, place_order=True)
            edit_menu = MenuForm(instance=menu)

        except Menu.DoesNotExist:
            raise Http404("Menu does not exist")

        return render(
            request, "kitchen/daily_menu.html", {"menu": edit_menu, "orders": orders}
        )

    def post(self, request, *args, **kwargs):
        """Modify a Menu

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to menu list
        """

        try:
            menu = get_object_or_404(Menu, date=kwargs["date"])
            edit_menu = MenuForm(request.POST, instance=menu)
            if edit_menu.is_valid():
                edit_menu.save()
                return redirect("index")

        except Menu.DoesNotExist:
            raise Http404("Menu does not exist")

        return render(request, "kitchen/daily_menu.html", {"menu": edit_menu})


class DeleteMenuView(LoginRequiredMixin, DeleteView):

    model = Menu
    success_url = reverse_lazy("index")


class PlateView(LoginRequiredMixin, View):
    def get(self, request):
        """Obtain all plates

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with all plates
        """
        plates = Plate.objects.all()
        add_plate = PlateForm()
        return render(
            request, "kitchen/plates.html", {"plates": plates, "form": add_plate}
        )

    def post(self, request):
        """Create a new Plate

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to plate list
        """
        add_plate = PlateForm(request.POST)
        if add_plate.is_valid():
            add_plate.save()
            return redirect("plate")

        return HttpResponse(
            request,
            status=422,
        )


class DeletePlateView(LoginRequiredMixin, DeleteView):

    model = Plate
    success_url = reverse_lazy("plate")


class EditPlateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Obtain a plate

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with a plate
        """
        plate = Plate.objects.get(pk=kwargs["pk"])
        add_plate = PlateForm(instance=plate)
        return render(request, "kitchen/edit_plates.html", {"form": add_plate})

    def post(self, request, *args, **kwargs):
        """Modify a Plate

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to plate list
        """
        try:
            plate = Plate.objects.get(pk=kwargs["pk"])
            edited_plate = PlateForm(request.POST, instance=plate)
            if edited_plate.is_valid():
                edited_plate.save()
                return redirect("plate")

            return HttpResponse(
                request,
                status=422,
            )
        except Plate.DoesNotExist:
            raise Http404("Plate does not exist")


class ClientMenuView(View):

    cl_now = datetime.now(pytz.timezone("America/Santiago"))
    today11am = cl_now.replace(hour=11, minute=00, second=0, microsecond=0)

    def get(self, request, *args, **kwargs):
        """Obtain a client order available only for the order of the day only before 11am CLT

        Args:
            request (HttpRequest): A get request

        Returns:
            HttpRequest: html view with the client order
        """
        try:
            order = get_object_or_404(Order, uuid=uuid.UUID(str(kwargs["order_id"])))
            if self.cl_now > self.today11am or self.cl_now.date() != order.menu.date:
                raise Http404("Menu not available")

            order_form = OrderForm(instance=order)
        except Menu.DoesNotExist:
            raise Http404("Order does not exist")

        return render(
            request,
            "kitchen/client_order.html",
            {"order_form": order_form, "order": order},
        )

    def post(self, request, *args, **kwargs):
        """Obtain a client order available only for the order of the day only before 11am CLT

        Args:
            request (HttpRequest): A post request

        Returns:
            HttpRequest: redirect to the client order
        """

        try:
            print(kwargs["order_id"])
            order = get_object_or_404(Order, uuid=uuid.UUID(str(kwargs["order_id"])))

            if self.cl_now > self.today11am or self.cl_now.date() != order.menu.date:
                raise Http404("Menu not available")

            edit_order = OrderForm(request.POST, instance=order)
            if edit_order.is_valid():
                edit_order.save()
                return redirect("client_menu", order_id=str(kwargs["order_id"]))

        except Menu.DoesNotExist:
            raise Http404("Order does not exist")

        return render(
            request,
            "kitchen/client_order.html",
            {"order_form": edit_order, "order": order},
        )
