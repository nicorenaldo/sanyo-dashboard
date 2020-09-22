from django import forms
from django.contrib.auth.models import User
from .models import Product,Kategori, Transaksi

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        exclude = ['image']

class IssueForm(forms.ModelForm):

    class Meta:
        model = Transaksi
        fields = ['sold_quantity','items','harga_terjual']
        widgets = {
            'items': forms.HiddenInput,
        }