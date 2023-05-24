from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Sector,  Production
from products.models import Product
from employees.models import Employee
from django.forms import model_to_dict

@login_required(login_url="/accounts/login/")
def SectorsListView(request):
    context = {
        "active_icon": "productions_sectors",
        "sectors": Sector.objects.all()
    }
    return render(request, "productions/sectors.html", context=context)


@login_required(login_url="/accounts/login/")
def SectorsAddView(request):
    context = {
        "active_icon": "productions_sectors",
        "sector_status": Sector.status.field.choices
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        # Check if a sector with the same attributes exists
        if Sector.objects.filter(**attributes).exists():
            messages.error(request, 'Sector already exists!',
                           extra_tags="warning")
            return redirect('productions:sectors_add')

        try:
            # Create the sector
            new_sector = Sector.objects.create(**attributes)

            # If it doesn't exists save it
            new_sector.save()

            messages.success(request, 'Sector: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('productions:sectors_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('productions:sectors_add')

    return render(request, "productions/sectors_add.html", context=context)


@login_required(login_url="/accounts/login/")
def SectorsUpdateView(request, sector_id):
    """
    Args:
        sector_id : The sector's ID that will be updated
    """

    # Get the sector
    try:
        # Get the sector to update
        sector = Sector.objects.get(id=sector_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the sector!', extra_tags="danger")
        print(e)
        return redirect('productions:sectors_list')

    context = {
        "active_icon": "productions_sectors",
        "sector_status": Sector.status.field.choices,
        "sector": sector
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }

            # Check if a sector with the same attributes exists
            if Sector.objects.filter(**attributes).exists():
                messages.error(request, 'Sector already exists!',
                               extra_tags="warning")
                return redirect('productions:sectors_add')

            # Get the sector to update
            sector = Sector.objects.filter(
                id=sector_id).update(**attributes)

            sector = Sector.objects.get(id=sector_id)

            messages.success(request, '¡Sector: ' + sector.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('productions:sectors_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('productions:sectors_list')

    return render(request, "productions/sectors_update.html", context=context)


@login_required(login_url="/accounts/login/")
def SectorsDeleteView(request, sector_id):
    """
    Args:
        sector_id : The sector's ID that will be deleted
    """
    try:
        # Get the sector to delete
        sector = Sector.objects.get(id=sector_id)
        sector.delete()
        messages.success(request, 'Sector: ' + sector.name +
                         ' deleted!', extra_tags="success")
        return redirect('productions:sectors_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('productions:sectors_list')


@login_required(login_url="/accounts/login/")
def ProductionsListView(request):
    context = {
        "active_icon": "productions",
        "productions": Production.objects.all()
    }
    return render(request, "productions/productions.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductionsAddView(request):
    context = {
        "active_icon": "productions_sectors",
        "sectors": Sector.objects.all().filter(status="ACTIVE"),
        "products": Product.objects.all().filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "product": Product.objects.get(id=data['product']),
            "description": data['description'],
            "sector": Sector.objects.get(id=data['sector']),
            "weight": data['weight'],
            "quantity": data['quantity'],
            "total_price": data['total_price']
        }

        # Check if a production with the same attributes exists
        if Production.objects.filter(**attributes).exists():
            messages.error(request, 'Production already exists!',
                           extra_tags="warning")
            return redirect('productions:productions_add')

        try:
            # Create the production
            new_production = Production.objects.create(**attributes)

            # If it doesn't exists save it
            new_production.save()

            messages.success(request, 'Production: ' +
                             attributes["product"] + ' created succesfully!', extra_tags="success")
            return redirect('productions:productions_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('productions:productions_add')

    return render(request, "productions/productions_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductionsUpdateView(request, production_id):
    """
    Args:
        production_id : The production's ID that will be updated
    """

    # Get the production
    try:
        # Get the production to update
        production = Production.objects.get(id=production_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the production!', extra_tags="danger")
        print(e)
        return redirect('productions:productions_list')

    context = {
        "active_icon": "productions",
        "production": production,
        "sectors": Sector.objects.all().filter(status="ACTIVE"),
        "products": Product.objects.all().filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        try:
            # Save the POST arguments
            data = request.POST

            if 'product' in data:
                product = Product.objects.get(id=data['product'])
            else:
                product = production.product

            attributes = {
                "product": product,
                "description": data['description'],
                "sector": Sector.objects.get(id=data['sector']),
                "weight": data['weight'],
                "quantity": data['quantity'],
                "total_price": data['total_price'],
            }

            # Check if a production with the same attributes exists
            if Production.objects.filter(**attributes).exclude(id=production_id).exists():
                messages.error(request, 'Production already exists!',
                               extra_tags="warning")
                return redirect('productions:productions_add')

            # Update the production
            Production.objects.filter(id=production_id).update(**attributes)

            messages.success(request, 'Production: ' + production.product +
                             ' updated successfully!', extra_tags="success")
            return redirect('productions:productions_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('productions:productions_list')

    return render(request, "productions/productions_update.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductionsDeleteView(request, production_id):
    """
    Args:
        production_id : The production's ID that will be deleted
    """
    try:
        # Get the production to delete
        production = Production.objects.get(id=production_id)
        production.delete()
        messages.success(request, '¡Production: ' + production.product +
                         ' deleted!', extra_tags="success")
        return redirect('productions:productions_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('productions:productions_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def GetProductionsAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            productions = Production.objects.filter(
                product__icontains=request.POST['term'])
            for production in productions[0:10]:
                item = production.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)

