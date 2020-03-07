from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def registerPage(request):
    form=CreateUserForm()
    if request.method=='POST':
      form = CreateUserForm(request.POST)
      if form.is_valid():
        form.save()
        user= form.cleaned_data.get('username')
        messages.success(request,'Account was created for '+user)
        return redirect('login/')

    context={'form':form}
    return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.method=='POST':
        request.POST.get('username')
        request.POST.get('password ')
        #user=authenticate(request,username=username,password=Password1)
    context={}
    return render(request,'accounts/login.html',context)

def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()

    total_customers= customers.count()
    total_ordrs=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='pending').count()

    context={'orders':orders,'customers':customers,'total_orders':total_ordrs,'pending':pending,'delivered':delivered}
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    context={'item':order}
    if request.method=='POST':
        order.delete()
        return redirect('/')
    return render(request,'accounts/delete.html',context)