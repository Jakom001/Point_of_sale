from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Group, Capital, Expense
from django.forms import model_to_dict

@login_required(login_url="/accounts/login/")
def GroupsListView(request):
    context = {
        "active_icon": "expenses_groups",
        "groups": Group.objects.all()
    }
    return render(request, "expenses/groups.html", context=context)


@login_required(login_url="/accounts/login/")
def GroupsAddView(request):
    context = {
        "active_icon": "expenses_groups",
        "group_status": Group.status.field.choices
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        # Check if a group with the same attributes exists
        if Group.objects.filter(**attributes).exists():
            messages.error(request, 'Group already exists!',
                           extra_tags="warning")
            return redirect('expenses:groups_add')

        try:
            # Create the group
            new_group = Group.objects.create(**attributes)

            # If it doesn't exists save it
            new_group.save()

            messages.success(request, 'Group: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('expenses:groups_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('expenses:groups_add')

    return render(request, "expenses/groups_add.html", context=context)


@login_required(login_url="/accounts/login/")
def GroupsUpdateView(request, group_id):
    """
    Args:
        group_id : The group's ID that will be updated
    """

    # Get the group
    try:
        # Get the group to update
        group = Group.objects.get(id=group_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the group!', extra_tags="danger")
        print(e)
        return redirect('expenses:groups_list')

    context = {
        "active_icon": "expenses_groups",
        "group_status": Group.status.field.choices,
        "group": group
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

            # Check if a group with the same attributes exists
            if Group.objects.filter(**attributes).exists():
                messages.error(request, 'Group already exists!',
                               extra_tags="warning")
                return redirect('expenses:groups_add')

            # Get the group to update
            group = Group.objects.filter(
                id=group_id).update(**attributes)

            group = Group.objects.get(id=group_id)

            messages.success(request, '¡Group: ' + group.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('expenses:groups_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('expenses:groups_list')

    return render(request, "expenses/groups_update.html", context=context)


@login_required(login_url="/accounts/login/")
def GroupsDeleteView(request, group_id):
    """
    Args:
        group_id : The group's ID that will be deleted
    """
    try:
        # Get the group to delete
        group = Group.objects.get(id=group_id)
        group.delete()
        messages.success(request, '¡Group: ' + group.name +
                         ' deleted!', extra_tags="success")
        return redirect('expenses:groups_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('expenses:groups_list')


@login_required(login_url="/accounts/login/")
def CapitalsListView(request):
    context = {
        "active_icon": "expenses_capitals",
        "capitals": Capital.objects.all()
    }
    return render(request, "expenses/capitals.html", context=context)


@login_required(login_url="/accounts/login/")
def CapitalsAddView(request):
    context = {
        "active_icon": "expenses_capitals",
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "source": data['source'],
            "amount": data['amount'],
            "description": data['description'],
        }

        try:
            # Create the capital
            new_capital = Capital.objects.create(**attributes)

            # If it doesn't exists save it
            new_capital.save()

            messages.success(request, 'Capital: created succesfully!', extra_tags="success")
            return redirect('expenses:capitals_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('expenses:capitals_add')

    return render(request, "expenses/capitals_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CapitalsUpdateView(request, capital_id):
    """
    Args:
        capital_id : The capital's ID that will be updated
    """

    # Get the capital
    try:
        # Get the capital to update
        capital = Capital.objects.get(id=capital_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the capital!', extra_tags="danger")
        print(e)
        return redirect('expenses:capitals_list')

    context = {
        "active_icon": "expenses_capitals",
        "capital": capital
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "source": data['source'],
                "amount": data['amount'],
                "description": data['description'],
            }


            # Get the capital to update
            capital = Capital.objects.filter(
                id=capital_id).update(**attributes)

            capital = Capital.objects.get(id=capital_id)

            messages.success(request, '¡Capital: updated successfully!', extra_tags="success")
            return redirect('expenses:capitals_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('expenses:capitals_list')

    return render(request, "expenses/capitals_update.html", context=context)


@login_required(login_url="/accounts/login/")
def CapitalsDeleteView(request, capital_id):
    """
    Args:
        capital_id : The capital's ID that will be deleted
    """
    try:
        # Get the capital to delete
        capital = Capital.objects.get(id=capital_id)
        capital.delete()
        messages.success(request, '¡Capital: deleted!', extra_tags="success")
        return redirect('expenses:capitals_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('expenses:capitals_list')
    

@login_required(login_url="/accounts/login/")
def ExpensesListView(request):
    context = {
        "active_icon": "expenses",
        "expenses": Expense.objects.all()
    }
    return render(request, "expenses/expenses.html", context=context)


@login_required(login_url="/accounts/login/")
def ExpensesAddView(request):
    context = {
        "active_icon": "expenses_groups",
        "groups": Group.objects.all().filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "description": data['description'],
            "group": Group.objects.get(id=data['group']),
            "amount": data['amount'],
            "name": data['name'],
        }

        # Check if a expense with the same attributes exists
        if Expense.objects.filter(**attributes).exists():
            messages.error(request, 'Expense already exists!',
                           extra_tags="warning")
            return redirect('expenses:expenses_add')

        try:
            # Create the expense
            new_expense = Expense.objects.create(**attributes)

            # If it doesn't exists save it
            new_expense.save()

            messages.success(request, 'Expense: ' +
                             attributes["name"] + ' created succesfully!', extra_tags="success")
            return redirect('expenses:expenses_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('expenses:expenses_add')

    return render(request, "expenses/expenses_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ExpensesUpdateView(request, expense_id):
    """
    Args:
        expense_id : The expense's ID that will be updated
    """

    # Get the expense
    try:
        # Get the expense to update
        expense = Expense.objects.get(id=expense_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the expense!', extra_tags="danger")
        print(e)
        return redirect('expenses:expenses_list')

    context = {
        "active_icon": "expenses",
        "expense": expense,
        "groups": Group.objects.all().filter(status="ACTIVE"),
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST


            attributes = {
                "description": data['description'],
                "group": Group.objects.get(id=data['group']),
                "amount": data['amount'],
                "name": data['name'],
            }

            # Check if a expense with the same attributes exists
            if expense.objects.filter(**attributes).exists():
                messages.error(request, 'Expense already exists!',
                               extra_tags="warning")
                return redirect('expenses:expenses_add')

            # Get the expense to update
            expense = Expense.objects.filter(
                id=expense_id).update(**attributes)

            expense = Expense.objects.get(id=expense_id)

            messages.success(request, '¡Expense: ' + expense.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('expenses:expenses_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('expenses:expenses_list')

    return render(request, "expenses/expenses_update.html", context=context)


@login_required(login_url="/accounts/login/")
def ExpensesDeleteView(request, expense_id):
    """
    Args:
        expense_id : The expense's ID that will be deleted
    """
    try:
        # Get the expense to delete
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        messages.success(request, '¡Expense: ' + expense.name +
                         ' deleted!', extra_tags="success")
        return redirect('expenses:expenses_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('expenses:expenses_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def GetExpensesAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            expenses = Expense.objects.filter(
                name__icontains=request.POST['term'])
            for expense in expenses[0:10]:
                item = expense.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)