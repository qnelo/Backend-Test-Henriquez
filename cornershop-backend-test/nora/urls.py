from datetime import datetime

from django.urls import path, register_converter

from . import views


class DateConverter:
    regex = "\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%d")

    def to_url(self, value):
        return value


register_converter(DateConverter, "yyyy")


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("delete/<int:pk>/", views.DeleteMenuView.as_view(), name="delete_menu"),
    path("<yyyy:date>/", views.DailyMenuView.as_view(), name="daily_menu"),
    path("plate/", views.PlateView.as_view(), name="plate"),
    path(
        "plate/delete/<int:pk>/", views.DeletePlateView.as_view(), name="delete_plate"
    ),
    path("plate/edit/<int:pk>/", views.EditPlateView.as_view(), name="edit_plate"),
    path("menu/<uuid:order_id>/", views.ClientMenuView.as_view(), name="client_menu"),
]
