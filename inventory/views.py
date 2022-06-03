from itertools import product
from unicodedata import name
from django.shortcuts import redirect, render
from carts.models import CartItem
from carts.views import cart
from inventory.forms import AddItemForm
from inventory.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url= 'login')
def crate_detail(request, category_slug, crate_slug):
    user = request.user
    try:
        # get crate object
        crate = Crate.objects.get(category__slug = category_slug, slug = crate_slug)

        # check if crate inside user cart
        carte_in_cart = CartItem.objects.filter(cart__user = user, crate = crate)
    except Exception as e:
        raise e

    try:
        # get items stored inside crate
        items = Item.objects.filter(crate = crate)
    except Exception as e:
        raise e

    if request.method == 'POST':
        # check if post request for change product status
        if "change_status" in request.POST:
            carte_status_list = request.POST['carte_status_list']
            crate.status = carte_status_list
            crate.save()

        if "change_quantity" in request.POST:
            quantity = request.POST['quantity']
            crate.stock = quantity
            crate.save()


        # check if post request for add new item
        if "add_item" in request.POST:
            item_name = request.POST['item_name']

            new_item = Item(
                crate = crate,
                item_name = item_name, 
                category = crate.category, 
                status = "Added",
                client = user.company,
                )
            new_item.save()
            new_item.slug = item_name.lower().replace(' ', '_')
            new_item.save()
            
    context = {
        'items': items,
        'crate': crate,
        'carte_in_cart': carte_in_cart,
    }
    return render(request, 'inventory/crate_detail.html', context)


@login_required(login_url= 'login')
def add_item(request, crate_slug):
    crate = Crate.objects.get(slug = crate_slug)
    context = {
        'crate': crate,
       
    }
    return render(request, 'inventory/add_item.html',  context)


@login_required(login_url= 'login')
def remove_item(request, category_slug, crate_slug, item_id):
    item = Item.objects.get(id = item_id)
    item.delete()    
    return redirect('crate_detail', category_slug, crate_slug)


@login_required(login_url= 'login')
def item_detail(request, category_slug, crate_slug, item_slug):
    user = request.user
    try:
        # get crate object
        crate = Crate.objects.get(category__slug = category_slug, slug = crate_slug)
    except Exception as e:
        raise e

    try:
        # get item object
        item = Item.objects.get(crate = crate, category__slug = category_slug, slug = item_slug)

        # get all the crates of client excluding item stored crate
        crates = Crate.objects.filter(client = user.company)

        # check if item inside the cart or not
        item_in_cart = CartItem.objects.filter(cart__user = user, item = item)
    except Exception as e:
        raise e


    # if request post
    if request.method == 'POST':
        # change item status
        if "change_status" in request.POST:
            item_status_list = request.POST['item_status_list']
            item.status = item_status_list
            item.save()

        # request change item location
        if "change_item_crate" in request.POST:
            change_item_crate = request.POST['item_location']
            change_crate = Crate.objects.get(crate_name = change_item_crate)
            item.change_crate = change_crate
            item.save()

        # approve change item location
        if "approve_change" in request.POST:
            item_change_location = request.POST['item_change_location']
            approved_crate = Crate.objects.get(crate_name = item_change_location)
            item.crate = approved_crate

            # check if changed successful
            if item.crate:
                item.change_crate = None
            item.save()
            

    context = {
        'crates': crates,
        'crate': crate,
        'item': item,
        'item_in_cart': item_in_cart,
    }

    return render(request, 'inventory/item_detail.html', context)