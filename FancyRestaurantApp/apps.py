from django.apps import AppConfig


class FancyRestaurantAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FancyRestaurantApp"
    label = "reservations"
