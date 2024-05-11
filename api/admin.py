from django.contrib import admin
from .models import Profile , Card , Favorite ,Product
# Register your models here.

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(Card)
