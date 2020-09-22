from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models import F, Sum
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    harga_jual = models.DecimalField(max_digits=14 , decimal_places=2)
    harga_modal = models.DecimalField(max_digits=14, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey('Kategori', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='poster/' , blank=True , null=True)
    slug = models.SlugField(blank=True , null=True)
    supplier = models.CharField(max_length=100,null=True,blank=True)

    def save(self, *args , **kwargs):
        if not self.slug and self.name :
            self.slug = slugify(self.name)
        super(Product , self).save(*args , **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('stock:detail_product', kwargs={'pk': self.pk , 'slug': self.slug})

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/user.jpg"

class Kategori(models.Model):
    category_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='kategori/' , blank=True , null=True)
    slug = models.SlugField(blank=True , null=True)
    def save(self, *args , **kwargs):
        if not self.slug and self.category_name :
            self.slug = slugify(self.category_name)
        super(Kategori , self).save(*args , **kwargs)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('stock:dashboard')

class Transaksi(models.Model):
    items = models.ForeignKey(Product,on_delete=models.PROTECT, null=True)
    purchase_date = models.DateTimeField(default=timezone.now)
    sold_quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    harga_terjual = models.DecimalField(max_digits=14, decimal_places=2, default=0)


    def save(self, *args, **kwargs):
        super(Transaksi, self).save(*args, **kwargs)
        self.items.quantity -= self.sold_quantity
        self.items.save()
    
    def delete(self, *args, **kwargs):
        self.items.quantity += self.sold_quantity
        self.items.save()
        super(Transaksi, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)
    
    @property
    def total(self):
        return int(self.sold_quantity * self.harga_terjual)


