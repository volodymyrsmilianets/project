from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    favorites = models.ManyToManyField(User, related_name='favorite_products', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новий'),
        ('ACCEPTED', 'Прийнято'),
        ('REJECTED', 'Відхилено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NEW')

    def __str__(self):
        return f"Замовлення №{self.id} від {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"