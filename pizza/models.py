from django.db import models

class PizzaOrder(models.Model):
    STATUS_CHOICES = [
        ("received","Order Received"),
        ("making","Being prepared"),
        ("baking","Baking"),
        ("shipping","Out for delivery"),
        ("delivered","Delivered"),
    ]

    customer_name = models.CharField(max_length=100)
    user_descriptn = models.TextField()
    ingrednts = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="received")
    chef_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pizza Order #{self.id} -> {self.customer_name}"


# Create your models here.
