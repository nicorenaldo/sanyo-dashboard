from .models import Product, Kategori, Transaksi
import django_filters
from django import forms
from datetime import datetime
class Filter(django_filters.FilterSet):
    CHOICES=[
        (1, 'Januari'),
        (2, 'Februari'),
        (3, 'Maret'),
        (4, 'April'),
        (5, 'Mei'),
        (6, 'Juni'),
        (7, 'Juli'),
        (8, 'Agustus'),
        (9, 'September'),
        (10, 'Oktober'),
        (11, 'November'),
        (12, 'Desember'),        
    ]

    purchase_month = django_filters.ChoiceFilter(choices=CHOICES, field_name='purchase_date', lookup_expr='month',empty_label=None)

    purchase_year = django_filters.NumberFilter(field_name='purchase_date', lookup_expr='year')

    class Meta:
        model = Transaksi
        fields = ['purchase_month','purchase_year']

class Filter2(django_filters.FilterSet):
 
    purchase_year = django_filters.NumberFilter(field_name='purchase_date', lookup_expr='year')

    class Meta:
        model = Transaksi
        fields = ['purchase_year']


