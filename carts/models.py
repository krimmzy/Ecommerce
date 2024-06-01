from django.db import models
from store.models import Product, Variation
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)

	def __str__(self):
		return f"cart_id - User: {self.user.username}"

class CartItem(models.Model):
	STATUS_CHOICES = [
		('active', 'Active'),
		('completed', 'Completed'),
		('cancelled','Cancelled'),
	]
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100, default='Unknown')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variations = models.ManyToManyField(Variation, blank=True)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	is_active = models.BooleanField(default=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

	def __str__(self):
		return f"CartItem - Cart: {self.cart}, Product: {self.product_name}, Status: {self.status}"

	def sub_total(self):
		return self.product.price * self.quantity

	def __unicode__(self):
		return self.product