from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from carts.models import *
from inventory.models import *


# add crate to cart.
@login_required(login_url= 'login')
def add_cart(request, product_id):
    # get crate object
    crate = Crate.objects.get(id = product_id)
    try:
        # check if cart exist 
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        # else create new cart object
        cart = Cart.objects.create(user = request.user)
        cart.save()

    try:
        # if already crate exist inside cart  
        cart_item = CartItem.objects.get(user = request.user, crate = crate)
        # add quantity by 1
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # else create new cart item object
        cart_item = CartItem.objects.create(
            user = request.user,
            crate = crate,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

# add item to cart.
@login_required(login_url= 'login')
def add_item_cart(request, product_id):
    # get item object
    item = Item.objects.get(id = product_id)

    try:
         # check if cart exist 
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
         # else create new cart object
        cart = Cart.objects.create(user = request.user)
        cart.save()

    try:
        # if already item exist inside cart
        cart_item = CartItem.objects.get(user = request.user, item = item)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # else create new cart item object
        cart_item = CartItem.objects.create(
            user = request.user,
            item = item,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

        
@login_required(login_url= 'login')
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        # if user is_authenticated
        if request.user.is_authenticated:
            # then get user cart
            cart = Cart.objects.get(user = request.user)
            # get user cart items
            cart_items = CartItem.objects.filter(user=request.user, cart = cart, is_active=True)
       
        # calculate total of cart items   
        for cart_item in cart_items:
            quantity += cart_item.quantity
            if cart_item.crate is None:
                total += (cart_item.item.delivery_price * cart_item.quantity)
            else:
                total += (cart_item.crate.delivery_price * cart_item.quantity)
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'inventory/cart.html', context)


# remove crate
@login_required(login_url= 'login')
def remove_cart(request, product_id):
    crate = get_object_or_404(Crate, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, crate=crate)

        # if crate quantity > 1 then minus by one else remove 
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# remove Item
@login_required(login_url= 'login')
def remove_cart_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    try:
        if request.user.is_authenticated:
            # if item quantity > 1 then minus by one else remove 
            cart_item = CartItem.objects.get(user=request.user, item=item)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
    

@login_required(login_url= 'login')
def delete_cart_crate(request, product_id):
    crate = get_object_or_404(Crate, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(crate=crate, user=request.user)

    # delete crate
    cart_item.delete()
    return redirect('cart')


@login_required(login_url= 'login')
def delete_cart_item(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(item=item, user=request.user)

    # delete item
    cart_item.delete()
    return redirect('cart')