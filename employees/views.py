from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Employee, Shop



@login_required(login_url="/accounts/login/")
def ShopsListView(request):
    context = {
        "active_icon": "employees_shops",
        "shops": Shop.objects.all()
    }
    return render(request, "employees/shops.html", context=context)


@login_required(login_url="/accounts/login/")
def ShopsAddView(request):
    context = {
        "active_icon": "employees_shops",
        "shop_status": Shop.status.field.choices,
        "employees": Employee.objects.all()
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "location":data['location'],
            "description": data['description'],
            "manager": Employee.objects.get(id=int(data['manager'])),
        }

        # Check if a shop with the same attributes exists
        if Shop.objects.filter(**attributes).exists():
            messages.error(request, 'Shop already exists!',
                           extra_tags="warning")
            return redirect('employees:shops_add')

        try:
            # Create the shop
            new_shop = Shop.objects.create(**attributes)

            # If it doesn't exists save it
            new_shop.save()

            messages.success(request, 'Shop: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('employees:shops_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('employees:shops_add')

    return render(request, "employees/shops_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ShopsUpdateView(request, shop_id):
    """
    Args:
        shop_id : The shop's ID that will be updated
    """

    # Get the shop
    try:
        # Get the shop to update
        shop = Shop.objects.get(id=shop_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the shop!', extra_tags="danger")
        print(e)
        return redirect('employees:shops_list')

    context = {
        "active_icon": "employees_shops",
        "shop_status": Shop.status.field.choices,
        "shop": shop,
        "employees": Employee.objects.all()
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
            "status": data['state'],
            "location":data['location'],
            "description": data['description'],
            "manager": Employee.objects.get(id=int(data['manager'])),
            }

            # Check if a shop with the same attributes exists
            if Shop.objects.filter(**attributes).exists():
                messages.error(request, 'Shop already exists!',
                               extra_tags="warning")
                return redirect('employees:shops_add')

            # Get the shop to update
            shop = Shop.objects.filter(
                id=shop_id).update(**attributes)

            shop = Shop.objects.get(id=shop_id)

            messages.success(request, '¡Shop: ' + shop.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('employees:shops_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('employees:shops_list')

    return render(request, "employees/shops_update.html", context=context)


@login_required(login_url="/accounts/login/")
def ShopsDeleteView(request, shop_id):
    """
    Args:
        shop_id : The shop's ID that will be deleted
    """
    try:
        # Get the shop to delete
        shop = Shop.objects.get(id=shop_id)
        shop.delete()
        messages.success(request, '¡Shop: ' + shop.name +
                         ' deleted!', extra_tags="success")
        return redirect('employees:shops_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('employees:shops_list')


@login_required(login_url="/accounts/login/")
def EmployeesListView(request):
    context = {
        "active_icon": "employees",
        "employees": Employee.objects.all()
    }
    return render(request, "employees/employees.html", context=context)


@login_required(login_url="/accounts/login/")
def EmployeesAddView(request):
    context = {
        "active_icon": "employees",
        "shops": Shop.objects.all().filter(status="ACTIVE")
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "salary": data['salary'],
            "shop": Shop.objects.get(id=data['shop']),
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a employee with the same attributes exists
        if Employee.objects.filter(**attributes).exists():
            messages.error(request, 'Employee already exists!',
                           extra_tags="warning")
            return redirect('employees:employees_add')

        try:
            # Create the employee
            new_employee = Employee.objects.create(**attributes)

            # If it doesn't exists save it
            new_employee.save()

            messages.success(request, 'Employee: ' + attributes["first_name"] + " " +
                             attributes["last_name"] + ' created succesfully!', extra_tags="success")
            return redirect('employees:employees_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('employees:employees_add')

    return render(request, "employees/employees_add.html", context=context)


@login_required(login_url="/accounts/login/")
def EmployeesUpdateView(request, employee_id):
    """
    Args:
        employee_id : The employee's ID that will be updated
    """

    # Get the employee
    try:
        # Get the employee to update
        employee = Employee.objects.get(id=employee_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the employee!', extra_tags="danger")
        print(e)
        return redirect('employees:employees_list')

    context = {
        "active_icon": "employees",
        "employee": employee,
        "shops": Shop.objects.all().filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "salary": data['salary'],
                "shop": Shop.objects.get(id=data['shop']),
                "email": data['email'],
                "phone": data['phone'],
            }

            # Check if a employee with the same attributes exists
            if Employee.objects.filter(**attributes).exists():
                messages.error(request, 'Employee already exists!',
                               extra_tags="warning")
                return redirect('employees:employees_add')

            # Get the employee to update
            employee = Employee.objects.filter(
                id=employee_id).update(**attributes)

            employee = Employee.objects.get(id=employee_id)

            messages.success(request, 'Employee: ' + employee.get_full_name() +
                             ' updated successfully!', extra_tags="success")
            return redirect('employees:employees_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('employees:employees_list')

    return render(request, "employees/employees_update.html", context=context)


@login_required(login_url="/accounts/login/")
def EmployeesDeleteView(request, employee_id):
    """
    Args:
        employee_id : The employee's ID that will be deleted
    """
    try:
        # Get the employee to delete
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        messages.success(request, '¡Employee: ' + employee.get_full_name() +
                         ' deleted!', extra_tags="success")
        return redirect('employees:employees_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('employees:employees_list')
