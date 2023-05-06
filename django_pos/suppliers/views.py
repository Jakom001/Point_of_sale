from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Supplier


@login_required(login_url="/accounts/login/")
def SuppliersListView(request):
    context = {
        "active_icon": "suppliers",
        "suppliers": Supplier.objects.all()
    }
    return render(request, "suppliers/suppliers.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersAddView(request):
    context = {
        "active_icon": "suppliers",
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "contact_person": data['contact_person'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a supplier with the same attributes exists
        if Supplier.objects.filter(**attributes).exists():
            messages.error(request, 'Supplier already exists!',
                           extra_tags="warning")
            return redirect('suppliers:suppliers_add')

        try:
            # Create the supplier
            new_supplier = Supplier.objects.create(**attributes)

            # If it doesn't exists save it
            new_supplier.save()

            messages.success(request, 'Supplier: ' + attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('suppliers:suppliers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('suppliers:suppliers_add')

    return render(request, "suppliers/suppliers_add.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersUpdateView(request, supplier_id):
    """
    Args:
        supplier_id : The supplierr's ID that will be updated
    """

    # Get the supplier
    try:
        # Get the supplier to update
        supplier = Supplier.objects.get(id=supplier_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the supplier!', extra_tags="danger")
        print(e)
        return redirect('suppliers:suppliers_list')

    context = {
        "active_icon": "suppliers",
        "supplier": supplier,
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
                "contact_person": data['contact_person'],
                "address": data['address'],
                "email": data['email'],
                "phone": data['phone'],
            }

            # Check if a supplier with the same attributes exists
            if Supplier.objects.filter(**attributes).exists():
                messages.error(request, 'supplier already exists!',
                               extra_tags="warning")
                return redirect('suppliers:suppliers_add')

            # Get the supplier to update
            supplier = Supplier.objects.filter(
                id=supplier_id).update(**attributes)

            supplier = Supplier.objects.get(id=supplier_id)

            messages.success(request, 'Supplier: ' + supplier.name() +
                             ' updated successfully!', extra_tags="success")
            return redirect('suppliers:suppliers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('suppliers:suppliers_list')

    return render(request, "suppliers/suppliers_update.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersDeleteView(request, supplier_id):
    """
    Args:
        supplier_id : The supplier's ID that will be deleted
    """
    try:
        # Get the supplier to delete
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        messages.success(request, 'supplier: ' + supplier.name +
                         ' deleted!', extra_tags="success")
        return redirect('suppliers:suppliers_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('suppliers:suppliers_list')
