from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    # Add any additional fields you want for the profile

    def __str__(self):
        return self.user.username
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cards_products_for_this_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='favorite_products_for_this_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
