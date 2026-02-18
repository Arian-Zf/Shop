from django.db import models
from shop.models import Product

class Order(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight <= 1000:
            return 20000
        elif weight <= 5000:
            return 30000
        else:
            return 40000
    
    def get_final_cost(self):
        price = self.get_total_cost() + self.get_post_cost()
        return price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.id}'
    
    def get_cost(self):
        return self.price * self.quantity
    
    def get_weight(self):
        return self.weight * self.quantity