from django.contrib import admin
from .models import Dish, DishImage, Connect, Payment

admin.site.register(Dish)
admin.site.register(DishImage)
admin.site.register(Connect)
admin.site.register(Payment)