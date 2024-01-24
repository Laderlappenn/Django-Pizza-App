from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import Users


class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Pizzas(models.Model):
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, verbose_name="Название пиццы")
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pizza_image = models.ImageField(null=True, blank=True, upload_to="orders/images/")
    class Meta:
        ordering = ['date_updated']
        # indexes = [models.Index(fields=['fieldname1', 'fieldname1']), ]

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    pizza = models.OneToOneField(Pizzas, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.quantity = self.quantity + 1
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.product.name


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.pizza.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)