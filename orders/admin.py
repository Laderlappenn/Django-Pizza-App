from django.contrib import admin
from .models import Pizzas, Category
# Register your models here.
admin.site.register(Pizzas)
admin.site.register(Category)