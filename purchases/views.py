from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from suppliers.models import Supplier
from products.models import Product
from weasyprint import HTML, CSS
from .models import Purchase, PurchaseDetail
import json
from django.shortcuts import render
import base64
import os
from django.contrib.staticfiles import finders
from django.template.loader import get_template


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def PurchasesListView(request):
    context = {
        "active_icon": "purchases",
        "purchases": Purchase.objects.all()
    }
    return render(request, "purchases/purchases.html", context=context)


@login_required(login_url="/accounts/login/")
def PurchasesAddView(request):
    context = {
        "active_icon": "purchases",
        "suppliers": [s.to_select2 for s in Supplier.objects.all()]
    }

    if request.method == 'POST':
        if is_ajax(request=request):
            # Save the POST arguements
            data = json.load(request)

            purchase_attributes = {
                "supplier": Supplier.objects.get(id=int(data['supplier'])),
                "sub_total": float(data["sub_total"]),
                "grand_total": float(data["grand_total"]),
                "tax_amount": float(data["tax_amount"]),
                "tax_percentage": float(data["tax_percentage"]),
                "amount_payed": float(data["amount_payed"]),
                "amount_change": float(data["amount_change"]),
            }
            try:
                # Create the purchase
                new_purchase = Purchase.objects.create(**purchase_attributes)
                new_purchase.save()
                # Create the purchase details
                products = data["products"]

                for product in products:
                    detail_attributes = {
                        "purchase": Purchase.objects.get(id=new_purchase.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "price": product["price"],
                        "weight":product['weight'],
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"],
                    }
                    purchase_detail_new = PurchaseDetail.objects.create(
                        **detail_attributes)
                    purchase_detail_new.save()

                print("Purchase saved")

                messages.success(
                    request, 'Purchase created succesfully!', extra_tags="success")

            except Exception as e:
                messages.success(
                    request, 'There was an error during the creation!', extra_tags="danger")

        return redirect('purchases:purchases_list')

    return render(request, "purchases/purchases_add.html", context=context)


@login_required(login_url="/accounts/login/")
def PurchasesDetailsView(request, purchase_id):
    """
    Args:
        purchase_id: ID of the purchase to view
    """
    try:
        # Get tthe purchase
        purchase = Purchase.objects.get(id=purchase_id)

        # Get the purchase details
        details = PurchaseDetail.objects.filter(purchase=purchase)

        context = {
            "active_icon": "purchases",
            "purchase": purchase,
            "details": details,
        }
        return render(request, "purchases/purchases_details.html", context=context)
    except Exception as e:
        messages.success(
            request, 'There was an error getting the purchase!', extra_tags="danger")
        print(e)
        return redirect('purchases:purchases_list')


@login_required(login_url="/accounts/login/")
def ReceiptPDFView(request, purchase_id):
    """
    Args:
        purchase_id: ID of the purchase to view the receipt
    """
    # Get the purchase
    purchase = Purchase.objects.get(id=purchase_id)

    # Get the purchase details
    details = PurchaseDetail.objects.filter(purchase=purchase)

    # Get the path to the image file
    image_path = finders.find('img/logo.png')

    # Read the image file and encode it as base64
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    template = get_template("purchases/purchases_receipt_pdf.html")
    context = {
        "purchase": purchase,
        "details": details,
        "company_logo": encoded_image,  # Pass the encoded image to the context
    }
    html_template = template.render(context)

    # CSS Bootstrap
    css_url = os.path.join(settings.BASE_DIR, 'static/css/receipt_pdf/bootstrap.min.css')

    # Create the PDF
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")
