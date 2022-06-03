from django.shortcuts import redirect, render
import datetime
import base64
import os
import re

from carts.models import CartItem
from inventory.models import Crate, Item
from orders.models import Order, OrderProduct, Return
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url= 'login')
def place_order(request, total=0, quantity=0,):
    user = request.user

    # get user cart products
    cart_products = CartItem.objects.filter(user = user)
    cart_product_count = cart_products.count()
    if cart_product_count < 0:
        return redirect('client_dashboard')

    
    grand_total = 0
    tax = 0

    # get payment info of each cart products
    for cart_product in cart_products:
        if cart_product.crate is None:
            total += (cart_product.item.delivery_price * cart_product.quantity)
        else:
            total += (cart_product.crate.delivery_price * cart_product.quantity)

        quantity += cart_product.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    delivery_date = datetime.date.today() + datetime.timedelta(days=1)

    # create new order
    order = Order()
    order.user = user
    order.company = user.company
    order.tax = tax
    order.order_total = grand_total
    order.ip = request.META.get('REMOTE_ADDR')
    order.delivery_date = delivery_date

    # get client location
    company_location = user.company.location
    order.company_location = company_location
    try:
        # try getting client branch location
        branch_location = user.branch.location
        order.branch_location = branch_location
    except Exception:
        pass
    
    order.save()

    # generate uniqe order number
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d") #20210305
    order_number = current_date + str(order.id)
    order.order_number = order_number
    order.save()

    context = {
        'order': order,
        'cart_products': cart_products,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'orders/place_order.html', context)


@login_required(login_url= 'login')
def order_complete(request):
    user = request.user
    order_number = 0

    # get order details
    if request.method == 'GET':
        order_number = request.GET['order_number']
        schedule = request.GET['schedule']
        schedule_duration = request.GET['schedule_duration']

        try:
            # set orderd details
            order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
            order.is_ordered = True
            order.schedule = schedule
            order.schedule_duration = schedule_duration
            order.save()
        except Order.DoesNotExist:
            # if product already ordered then set orderd status True
            order =  Order.objects.get(user=user, is_ordered=True, order_number=order_number)

    # Move the cart items to Order Product table
    cart_products = CartItem.objects.filter(user=request.user)


    for product in cart_products:
        # create crate added
        crate = Crate.objects.get(id=product.crate_id)
        if crate.client is None:
            for i in range(product.quantity):
                # uniqe name for crate
                encode = base64.b64encode(os.urandom(32))[:8]
                id = re.sub('\W+', '', str(encode))
                product_name = str(user.company) + "_crate_" + id

                #  create new crate and store inside pick-up-room
                new_crate = Crate.objects.create(
                status = "Ordered",
                client = user.company,
                category = product.crate.category,
                crate_name = product_name,
                slug = product_name.lower(),
                delivery_price = product.crate.delivery_price,
                return_price = product.crate.return_price,
                stock = 1
                )
                new_crate.save()

        # transfer cart products to orderproducts
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.crate_id = product.crate_id
        orderproduct.item_id = product.item_id
        orderproduct.quantity = product.quantity
        if crate.client is None:
            orderproduct.crate_id = new_crate.id

        # get price of ordred product
        if product.crate is None:
            orderproduct.product_price = product.item.delivery_price
        else:
            orderproduct.product_price = product.crate.delivery_price
        orderproduct.ordered = True
        orderproduct.save()

        # minus the quantity of the sold products & change warehouse location
        if product.crate is None:
            item = Item.objects.get(id=product.item_id)
            item.status = "Ordered"
            if item.stock > 0:
                item.stock -= product.quantity
            item.save()
        else:
            crate = Crate.objects.get(id=product.crate_id)
            crate.status = "Ordered"
            if crate.stock > 0:
                crate.stock -= product.quantity
            crate.save()
    

    # clear cart
    CartItem.objects.filter(user=request.user).delete()

    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    subtotal = 0
    for ordered_product in ordered_products:
        subtotal += ordered_product.product_price * ordered_product.quantity
    
    # get company name and location
    company = user.company
    location = company.location

    context = {
        'company': company,
        'location': location,
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'subtotal': subtotal,
        }
    return render(request, 'orders/order_complete.html', context)


@login_required(login_url= 'login')
def return_crate(request, crate_id):
    user = request.user

    # get return crate object
    crate = Crate.objects.get(id = crate_id)

    # get crate return price
    return_price = crate.return_price

    # calculate return tax, total
    tax = (2 * return_price)/100
    return_total = return_price + tax

    pickup_date = datetime.date.today() + datetime.timedelta(days=1)

    return_product = Return(
        user = user,
        company = user.company,
        crate = crate,
        tax = tax,
        pickup_date = pickup_date,
        return_total = return_total
    )
    return_product.save()

    # generate uniqe return number
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d") #20210305
    return_number = current_date + str(return_product.id)
    return_product.return_number = return_number
    return_product.save()

    context = {
        'company_location': user.company.location,
        'user': user,
        'return_product': return_product,
        'total': return_price,
        'tax': tax,
        'grand_total': return_total,
    }
    return render(request, 'orders/return_order.html', context)


@login_required(login_url= 'login')
def return_item(request, item_id):
    user = request.user

    # get return item object
    item = Item.objects.get(id = item_id)

    # get all the crates of client excluding item stored crate
    # crates = Crate.objects.filter(client = user.company).exclude(item__crate = item.crate)

    # get crate return price
    return_price = item.return_price

    # calculate return tax, total
    tax = (2 * return_price)/100
    return_total = return_price + tax
    pickup_date = datetime.date.today() + datetime.timedelta(days=1)

    return_product = Return(
        user = user,
        item = item,
        tax = tax,
        pickup_date = pickup_date,
        return_total = return_total
    )
    return_product.save()

    # generate uniqe return number
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d") #20210305
    return_number = current_date + str(return_product.id)
    return_product.return_number = return_number
    return_product.save()

    context = {
        'company_location': user.company.location,
        'user': user,
        'return_product': return_product,
        'total': return_price,
        'tax': tax,
        'grand_total': return_total,
    }
    return render(request, 'orders/return_order.html', context)


@login_required(login_url= 'login')
def initiat_return(request):
    user = request.user
    return_number = 0
    if request.method == 'GET':
        # get return number
        return_number = request.GET['return_number']

        try:
            # set return_order status True
            return_order =  Return.objects.get(user=user, returned=False, return_number=return_number)
            return_order.returned = True
            return_order.save()

            # change item status
            if return_order.item:
                item = Item.objects.get(id = return_order.item.id)
                item.status = "Return initiated"
                item.save()

            else:
                # change crate status
                crate = Crate.objects.get(id = return_order.crate.id)
                crate.status = "Return initiated"
                crate.save()
                
        except Return.DoesNotExist:
            # if product already ordered then set orderd status True
            return_order =  Return.objects.get(user=user, returned=True, return_number=return_number)
            
        company = user.company
        location = company.location

        context = {
            'return_order': return_order,
            'company': company,
            'location': location,
            }
    return render(request, 'orders/return_initiated.html', context)