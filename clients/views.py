from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from inventory.models import *
from carts.models import *
from orders.models import *


# Create your views here.
@login_required(login_url= 'login')
def client_dashboard(request):
    user = request.user

    if user.is_client:
        # get client orders
        orders = Order.objects.order_by('-created_at').filter(company=user.company, is_ordered=True)
        total_orders = orders.count()

         # get client orders
        return_orders = Return.objects.order_by('-created_at').filter(company=user.company, returned=True)
        total_returns = return_orders.count()

        user = request.user
        company = user.company

        # get all crates of client
        crates = Crate.objects.all().order_by('-created_date').filter(client = company)

        context = {
            'total_orders': total_orders,
            'total_returns': total_returns,
            'user': user,
            'company': company,
            'crates': crates
        }
        return render(request, 'clients/dashboard.html', context)
    elif user.is_staff:
        return redirect("dasboard_packford")
    else:
        return HttpResponse("Unable identify User")
    

@login_required(login_url= 'login')
def order_crate(request):
    user = request.user

    # get all crate where client__isnull
    # if client is null, then crate is new
    crates = Crate.objects.all().filter(client__isnull = True)

    context = {
        'user': user,
        'company': user.company,
        'crates': crates
    }
    return render(request, 'clients/order_crate.html', context)


@login_required(login_url= 'login')
def order_details(request, order_id):

    # ge client order from list of orders
    order_products = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    
    # calculate subtotal for order products 
    for order_product in order_products:
        subtotal += order_product.product_price * order_product.quantity

    location = order.company_location
    company = order.company

    context = {
        'company': company,
        'location': location,
        'order_products': order_products,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_details.html', context)


@login_required(login_url= 'login')
def list_order(request):
    user = request.user
     # get client order 
    orders = Order.objects.order_by('-created_at').filter(company = user.company, is_ordered=True)
    total_orders = orders.count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        }

    return render(request, 'orders/list_order.html', context)


@login_required(login_url= 'login')
def list_return(request):
    user = request.user
     # get client return order 
    return_orders = Return.objects.order_by('-created_at').filter(company = user.company, returned=True)
    total_returns = return_orders.count()

    # get phone
    phone = request.user.company.location.phone

    context = {
        'phone': phone,
        'return_orders': return_orders,
        'total_returns': total_returns,
        }

    return render(request, 'orders/list_return.html', context)


@login_required(login_url= 'login')
def return_details(request, return_id):
    return_products = Return.objects.get(return_number=return_id)

    company = return_products.company
    location = company.location
    print(company)

    context = {
        'company': company,
        'location': location,
        'return_products': return_products,
    }
    return render(request, 'orders/return_details.html', context)
