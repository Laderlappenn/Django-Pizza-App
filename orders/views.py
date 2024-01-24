from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from .models import Pizzas, OrderItem, Order
from users.models import Users

from .extras import generate_order_id


def index(request):
    queryset = Pizzas.objects.all().order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/index.html', {'pizzas': queryset, 'page_obj': page_obj})

def pizza_all(request):

    queryset = Pizzas.objects.all().order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})

def pizza_meat(request):

    queryset = Pizzas.objects.all().filter(category=1).order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})

def pizza_veg(request):

    queryset = Pizzas.objects.all().filter(category=2).order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})


def pizza_grill(request):

    queryset = Pizzas.objects.all().filter(category=3).order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})


def pizza_hot(request):

    queryset = Pizzas.objects.all().filter(category=4).order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})


def pizza_closed(request):

    queryset = Pizzas.objects.all().filter(category=5).order_by('-date_updated')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/components/pizza_component.html', {'pizzas': queryset, 'page_obj': page_obj})

@login_required
def add_to_cart(request, **kwargs):
    # cringe?
    auth_user_id = request.session.get('_auth_user_id')
    user = get_object_or_404(Users, pk=auth_user_id) #user=request.user doesnt work

    pizza = Pizzas.objects.filter(id=kwargs.get('item_id',"")).first()
    # create orderItem of the selected product
    order_pizza, status = OrderItem.objects.get_or_create(pizza=pizza)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user, is_ordered=False)
    user_order.items.add(order_pizza)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()
    order_pizza.save()
    return redirect(reverse('orders:index'))

@login_required
def get_user_pending_order(request):
    # get order for the correct user
    auth_user_id = request.session.get('_auth_user_id')
    user = get_object_or_404(Users, pk=auth_user_id)  # user=request.user doesnt work
    order = Order.objects.filter(owner=user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order

    }

    return render(request, 'orders/cart.html', context)