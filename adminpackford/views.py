from audioop import reverse
from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from accounts.forms import AddEmployeeForm
from clients.models import *
from accounts.models import User
from clients.forms import *
from django.db import IntegrityError
from inventory.models import Crate, Item
from orders.models import Order, Return
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url= 'login')
def dasboard_packford(request):
    user = request.user
    if user.is_staff:

        # get all companies
        companies = Company.objects.all()
        total_companies = companies.count()

        # get all branch
        branch = Branch.objects.all()
        total_branch = branch.count()

        if request.method == 'POST':
            company_name = request.POST['company_name']
            postcode = request.POST['postcode']
            address = request.POST['address']
            city = request.POST['city']
            country = request.POST['country']
            phone = request.POST['phone']
            
            location = Location(
                postcode = postcode,
                address = address,
                city = city,
                country = country,
                phone = phone
            )
            location.save()

            company = Company(company_name = company_name, location = location)
            company.save()
        context = {
            'companies': companies,
            'total_companies': total_companies,
            'total_branch': total_branch
        }
        return render(request, 'adminpackford/admin_dashboard.html', context)
    elif user.is_client:
        return redirect("client_dashboard")
    else:
        return HttpResponse("<h1>Error: Unable identify User</h1>")


@login_required(login_url= 'login')
def add_company(request):
    return render(request, 'adminpackford/add_company.html')


@login_required(login_url= 'login')
def company_detail(request, company_id):

    # get company 
    company = Company.objects.get(id = company_id)

     # get branches of company
    branches = Branch.objects.filter(company=company)
    total_branches = branches.count()

    # get company employees
    employees = User.objects.filter(company= company, branch__isnull=True)
    total_employees = employees.count()

    # get orders
    orders = Order.objects.order_by('-created_at').filter(company=company, is_ordered=True)
    total_orders = orders.count()

    # get client orders total amount
    total_order_amount = 0
    if request.user.is_accounter:
        for order in orders:
            total_order_amount += order.order_total
    
    # get retuens
    return_orders = Return.objects.order_by('-created_at').filter(company=company, returned=True)
    total_returns = return_orders.count()

    # get client return total amount
    total_return_amount = 0
    if request.user.is_accounter:
        for return_order in return_orders:
            total_return_amount += return_order.return_total

    # get client all crates
    crates = Crate.objects.filter(client = company)
    
    # check if request method is post
    if request.method == 'POST':

        addEmployeeForm = AddEmployeeForm(request.POST)
        branchForm = BranchForm(request.POST)

        # if post request for add employee
        if "add_employee" in request.POST:
            if addEmployeeForm.is_valid():
                first_name = addEmployeeForm.cleaned_data['first_name']
                last_name = addEmployeeForm.cleaned_data['last_name']
                username = addEmployeeForm.cleaned_data['username']
                email = addEmployeeForm.cleaned_data['email']
                password = request.POST["password"]
                confirmation = request.POST["confirmation"]

                if password != confirmation:
                    return render(request, 'adminpackford/add_employee.html', {
                        "message": "Passwords must match."
                    })

                # Attempt to create new user(employee)
                try:
                    employee = User.objects.create_user(username, email, password)
                    employee.save()
                except IntegrityError:
                    return render(request, 'adminpackford/add_employee.html', {
                        "message": "Username already taken."
                    })
                employee.first_name = first_name
                employee.last_name = last_name
                employee.is_client = True
                employee.company = company
                employee.save()

        # if post request for add branch
        if "add_branch" in request.POST:
            if branchForm.is_valid():
                branch_name = request.POST['branch_name']
                postcode = request.POST['postcode']
                address = request.POST['address']
                city = request.POST['city']
                country = request.POST['country']
                phone = request.POST['phone']

                location = Location(
                    postcode = postcode,
                    address = address,
                    city = city,
                    country = country,
                    phone = phone,
                )
                location.save()

                # add branch
                branch = Branch(
                    company = company, 
                    branch_name = branch_name, 
                    location = location
                    )
                branch.save()
        

    context = {
        'company': company,
        'branches': branches,
        'employees': employees,
        'crates': crates,
        'orders': orders,
        'return_orders': return_orders,
        'total_employees': total_employees,
        'total_orders': total_orders,
        'total_branches': total_branches,
        'total_returns': total_returns,
        'total_order_amount': total_order_amount,
        'total_return_amount': total_return_amount
    }
    
    return render(request, 'adminpackford/company_details.html', context)


@login_required(login_url= 'login')
def add_branch(request, company_id):
    company = Company.objects.get(id = company_id)

    # create new branch form
    branchForm = BranchForm()

    context = {
        'branchForm': branchForm,
        'company': company
    }
    return render(request, 'adminpackford/add_branch.html', context)


@login_required(login_url= 'login')
def branch_detail(request, company_id, branch_id):

    # get company, branch and branch employees
    company = Company.objects.get(id = company_id)
    branch = Branch.objects.get(id = branch_id)
    employees = User.objects.filter(branch= branch)

    # if post request for add employee
    addEmployeeForm = AddEmployeeForm(request.POST)
    if request.method == 'POST':
        if addEmployeeForm.is_valid():
            first_name = addEmployeeForm.cleaned_data['first_name']
            last_name = addEmployeeForm.cleaned_data['last_name']
            username = addEmployeeForm.cleaned_data['username']
            email = addEmployeeForm.cleaned_data['email']
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]

            if password != confirmation:
                return render(request, 'adminpackford/add_employee.html', {
                    "message": "Passwords must match."
                })

            # Attempt to create new user(employee)
            try:
                employee = User.objects.create_user(username, email, password)
                employee.save()
            except IntegrityError:
                return render(request, 'adminpackford/add_employee.html', {
                    "message": "Username already taken."
                })
            employee.first_name = first_name
            employee.last_name = last_name
            employee.is_client = True
            employee.company = company
            employee.branch = branch
            employee.save()


    context = {
        'company': company,
        'branch': branch,
        'employees': employees,
    }
    
    return render(request, 'adminpackford/branch_details.html', context)


@login_required(login_url= 'login')
def add_company_employee(request, company_id):
    company = Company.objects.get(id = company_id)

    # create new add employee form for company
    addEmployeeForm = AddEmployeeForm()
    context = {
        'company': company,  
        'addEmployeeForm': addEmployeeForm
    }
    return render(request, 'adminpackford/add_employee.html', context)


@login_required(login_url= 'login')
def add_branch_employee(request, company_id, branch_id):
    company = Company.objects.get(id = company_id)
    branch = Branch.objects.get(id= branch_id)

    # create new add employee form for branch
    addEmployeeForm = AddEmployeeForm()

    context = {
        'branch': branch,
        'company': company,  
        'addEmployeeForm': addEmployeeForm
    }
    return render(request, 'adminpackford/add_employee.html', context)


@login_required(login_url= 'login')
def all_order(request):
    # get all order
    orders = Order.objects.order_by('-created_at').filter(is_ordered=True)

    context = {
        'orders': orders,
    }
    return render(request, 'orders/list_order.html', context)


def all_return(request):
    # get all returns
    return_orders = Return.objects.order_by('-created_at').filter(returned=True)

    context = {
        'return_orders': return_orders,
    }
    return render(request, 'orders/list_return.html', context)


def change_item_location(request):
    items = Item.objects.filter(change_crate__isnull = False)

    context = {
        'items': items,
    }
    return render(request, 'adminpackford/request_change.html', context)

    

