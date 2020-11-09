from django.db.models.signals import post_save
from django.dispatch import receiver
from food.models import Dry, Guaranteed, Calorie, Food
from library.feeds import dried


@receiver(post_save, sender=Guaranteed)
def update_food(sender, instance, created, **kwargs):

    d = {
        'protein': dried(instance.protein, instance.moisture),
        'fat': dried(instance.fat, instance.moisture),
        'ash': dried(instance.ash, instance.moisture),
        'taurine': dried(instance.taurine, instance.moisture),
        'calcium': dried(instance.calcium, instance.moisture),
        'phosphorus': dried(instance.phosphorus, instance.moisture),
        'magnesium': dried(instance.magnesium, instance.moisture),
        'epa': dried(instance.epa, instance.moisture),
        'dha': dried(instance.dha, instance.moisture),
        'omega3': dried(instance.omega3, instance.moisture),
        'omega6': dried(instance.omega6, instance.moisture),
        'fibre': dried(instance.fibre, instance.moisture),
        'carbs': dried(instance.carbs, instance.moisture),
    }

    obj, created = Dry.objects.update_or_create(
        food_id=instance.food_id,
        defaults=d,
    )

    e = {
        'food_id': instance.food_id,
        'protein': instance.protein * 3.5,
        'fat': instance.fat * 8.5,
        'carbs': instance.carbs * 3.5,
        'total': 0,
    }

    e['total'] = e['protein'] + e['fat'] + e['carbs']

    obj, created = Calorie.objects.update_or_create(
        food_id=instance.food_id,
        defaults=e,
    )


