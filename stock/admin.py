from django.contrib import admin

# Register your models here.
from .models import Product, Kategori, Transaksi
admin.site.register(Product)
admin.site.register(Kategori)
admin.site.register(Transaksi)