from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Kategori, Transaksi
from django.db.models import Count, Q, Sum, F, Value
from .forms_submit import IssueForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from datetime import datetime
import calendar
from .filters import Filter, Filter2
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.


def browse (request):
    category = None
    listproduct = Product.objects.all()
    listkategori = Kategori.objects.annotate(totalkategori = Count('product'))
    harga = request.GET.get('harga', None)
    nama = request.GET.get('nama', None)

    search_query= request.GET.get('q')
    if search_query :
        listproduct = listproduct.filter(
            Q(name__icontains = search_query)|
            Q(description__icontains = search_query)
        )
	

    if harga == "hargaplus":
        listproduct = listproduct.order_by('harga_jual')
    elif harga == "hargamin":
        listproduct = listproduct.order_by('-harga_jual')
    
    if nama == "namaplus":
        listproduct = listproduct.order_by('name')
    elif nama == "namamin":
        listproduct = listproduct.order_by('-name')


    if request.is_ajax():
        html = render_to_string(
            template_name="stock/results-partial.html", 
            context={"list_product": listproduct}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    # paginator = Paginator(listproduct, 40)
    # page_number = request.GET.get('page')
    # listproduct = paginator.get_page(page_number)
    template = 'stock/dashboard.html'
    
    context = {'list_product' : listproduct , 'list_kategori' : listkategori}
    return render(request, template , context)

def ListEarning (request):
    data = request.GET.copy()

    if 'purchase_month' not in data:
        data['purchase_month'] = datetime.now().month

    if 'purchase_year' not in data: 
        data['purchase_year'] = datetime.now().year
    
    data_hari = Transaksi.objects.all().annotate(date=TruncDate('purchase_date')).values('date').annotate(total_sales=Sum(F('harga_terjual')*F('sold_quantity')))
    data_filter = Filter(data, queryset=data_hari)
    month = calendar.month_name[int(data_filter.data['purchase_month'])]
    month_earning = Transaksi.objects.filter(purchase_date__month=data['purchase_month']).annotate(date=TruncMonth('purchase_date')).values('date').annotate(total_sales=Sum(F('harga_terjual')*F('sold_quantity')), total_margin=Sum( ( F('harga_terjual')-F('items__harga_modal') )*F('sold_quantity') ))

    template = 'stock/profit.html'
    
    context = {'filter': data_filter, 'month': month, 'month_earning' : month_earning }
    return render(request, template , context)

def ListEarning_Year (request):
    data = request.GET.copy()

    if 'purchase_year' not in data: 
        data['purchase_year'] = datetime.now().year
    
    data_bulan = Transaksi.objects.filter(purchase_date__year=data['purchase_year']).annotate(date=TruncMonth('purchase_date')).values('date').annotate(total_sales=Sum(F('harga_terjual')*F('sold_quantity')),  total_margin=Sum( ( F('harga_terjual')-F('items__harga_modal') )*F('sold_quantity') ))

    data_filter = Filter2(data, queryset=data_bulan)

    year_earning = Transaksi.objects.filter(purchase_date__year=data['purchase_year']).annotate(date=TruncYear('purchase_date')).values('date').annotate(total_sales=Sum(F('harga_terjual')*F('sold_quantity')),  total_margin=Sum( ( F('harga_terjual')-F('items__harga_modal') )*F('sold_quantity') ))
    
    template = 'stock/profit_year.html'
    
    context = {'filter': data_filter, 'year_earning' : year_earning}
    return render(request, template , context)
    
def chart(request):
    data = request.GET.copy()

    if 'purchase_month' not in data:
        data['purchase_month'] = datetime.now().month

    if 'purchase_year' not in data: 
        data['purchase_year'] = datetime.now().year
    
    data_hari = Transaksi.objects.filter(purchase_date__month=data['purchase_month']).annotate(date=TruncDate('purchase_date')).values('date').annotate( total_sales=Sum( F('harga_terjual')*F('sold_quantity')), total_margin=Sum( ( F('harga_terjual')-F('items__harga_modal') )*F('sold_quantity') )).values('date','total_sales','total_margin')

    data_filter = Filter(data, queryset=data_hari)
    month = calendar.month_name[int(data_filter.data['purchase_month'])]
    
    data_product = Transaksi.objects.filter(purchase_date__month=data['purchase_month']).values('items__category__category_name').annotate(total_quantity=Sum('sold_quantity'))
    
    template = 'stock/chart.html'  
    context = { 'filter' : data_filter, 'month': month, 'data_product' : data_product }
    return render(request, template , context)
  
def year_chart(request):
    data = request.GET.copy()

    if 'purchase_year' not in data: 
        data['purchase_year'] = datetime.now().year
    
    data_bulan = Transaksi.objects.filter(purchase_date__year=data['purchase_year']).annotate(date=TruncMonth('purchase_date')).values('date').annotate( total_sales=Sum( F('harga_terjual')*F('sold_quantity')), total_margin=Sum( ( F('harga_terjual')-F('items__harga_modal') )*F('sold_quantity') )).values('date','total_sales','total_margin')

    data_filter = Filter2(data, queryset=data_bulan)
    year = data_filter.data['purchase_year']
    
    data_product = Transaksi.objects.filter(purchase_date__year=data['purchase_year']).values('items__category__category_name').annotate(total_quantity=Sum('sold_quantity'))
    
    template = 'stock/year_chart.html'  
    context = { 'filter' : data_filter, 'year': year, 'data_product' : data_product }
    return render(request, template , context)
  
def manage_categories(request, slug=None):
    listkategori = Kategori.objects.annotate(totalkategori = Count('product'))
    template = 'stock/categories.html'  
    context = { 'list_kategori' : listkategori}
    return render(request, template , context)

class ListTransaksi(ListView):
    model = Transaksi
    paginate_by = 100
    template_name = 'stock/transaksi.html'
    context_object_name = "data_transaksi"
    ordering = ['-purchase_date']

class DetailViewss(FormMixin, DetailView):
    model = Product
    template_name = 'stock/detail.html'  
    form_class = IssueForm
    
    def get_success_url(self):
        return reverse('stock:detail_product', kwargs={'slug': self.object.slug , 'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(DetailViewss, self).get_context_data(**kwargs)
        data_transaksi = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        daftar_transaksi = data_transaksi.transaksi_set.all()
        daftar_transaksi = daftar_transaksi.order_by('-purchase_date')
        paginator = Paginator(daftar_transaksi,15)
        page = self.request.GET.get('page')
        daftar_transaksi = paginator.get_page(page)
        context['form'] = IssueForm(initial={
            'items': data_transaksi,
            'sold_quantity' : 1,
            'harga_terjual' : data_transaksi.harga_jual
        })
        context["detail_product"] = self.object
        context['data_transaksi'] = daftar_transaksi
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(DetailViewss, self).form_valid(form)

def delete_transaksi(request, id):
    query = get_object_or_404(Transaksi, id=id)
    query.delete()
    return HttpResponseRedirect(reverse('stock:dashboard'))

class ProductCreate(CreateView):
    model = Product
    fields = ['name','description','harga_modal','supplier','harga_jual','quantity','category','image']
    success_url = '/'
    template_name = 'stock/submit.html'
    def form_valid(self, form):
        aa = form.save(commit=False)
        aa.save()
        return super().form_valid(form)

class ProductUpdate(UpdateView):
    model = Product
    fields = ['name','description','harga_modal','harga_jual','quantity','category','image']
    template_name = 'stock/post_update.html'
    def test_func(self):
        return True

class ProductDelete(DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        return True

class CategoryCreate( CreateView):
    model = Kategori
    fields = ['category_name']
    
    template_name = 'stock/submit.html'
    def form_valid(self, form):
        return super().form_valid(form)

class CategoryUpdate(UpdateView):
    model = Kategori
    fields = ['category_name']
    template_name = 'stock/post_update.html'
    def test_func(self):
        return True

class CategoryDelete(DeleteView):
    model = Kategori
    success_url = '/'

    def test_func(self):
        return True

class TransaksiDelete(DeleteView):
    model = Transaksi
    success_url = '/'

    def test_func(self):
        return True
    
    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        items = self.object.items
        return reverse_lazy( 'stock:detail_product', kwargs={'pk': items.pk , 'slug':items.slug})

class RecentTransaksiDelete(DeleteView):
    model = Transaksi
    success_url = '/'

    def test_func(self):
        return True
    
    def get_success_url(self):
        return reverse( 'stock:transaction_list')
