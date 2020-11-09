from django.apps import AppConfig


class FoodConfig(AppConfig):
    name = 'food'

    def ready(self):
        import food.signals
