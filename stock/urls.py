from django.urls import path, re_path
from . import views
from stock.views import DetailViewss, ProductCreate, ProductDelete, ProductUpdate,CategoryCreate, CategoryUpdate,CategoryDelete, ListTransaksi, TransaksiDelete, RecentTransaksiDelete
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.browse, name='dashboard'),

    # path('<x:pk>/delete/', views.delete_transaksi, name='transaksi-delete'),
    # path('delete/<int:id>/', views.delete_transaksi, name='transaksi-delete'),

    path('<int:pk>-<slug:slug>/', DetailViewss.as_view(), name='detail_product'),
    
    path('transaksi/', ListTransaksi.as_view(), name='transaction_list'),
    path('earnings/', views.ListEarning, name='earnings'),
    path('earnings/year/', views.ListEarning_Year, name='earnings_year'),
    path('chart/', views.chart, name='chart'),
    path('year_chart/', views.year_chart, name='year_chart'),

    path('submit/', ProductCreate.as_view(), name='author-add'),
    path('submitkategori/', CategoryCreate.as_view(), name='category-add'),

    path('<int:pk>-<slug:slug>/update/', ProductUpdate.as_view(), name='author-update'),
    path('<int:pk>-<slug:slug>/delete/', ProductDelete.as_view(), name='author-delete'),
    
    path('<slug:slug>/update/', CategoryUpdate.as_view(), name='category-update'),
    path('<slug:slug>/delete/', CategoryDelete.as_view(), name='category-delete'),

    path('transaksi/<int:pk>/delete/', TransaksiDelete.as_view(), name='transaksi-delete'),
    path('recent/<int:pk>/delete/', RecentTransaksiDelete.as_view(), name='recent-transaksi-delete'),
]

app_name='stock'