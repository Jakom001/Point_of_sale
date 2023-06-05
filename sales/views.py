from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from products.models import Product
from weasyprint import HTML, CSS
from .models import Sale, SaleDetail
import json
from django.shortcuts import render
import base64
import os
from django.contrib.staticfiles import finders
from django.template.loader import get_template


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def SalesListView(request):
    context = {
        "active_icon": "sales",
        "sales": Sale.objects.all()
    }
    return render(request, "sales/sales.html", context=context)


@login_required(login_url="/accounts/login/")
def SalesAddView(request):
    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()]
    }

    if request.method == 'POST':
        if is_ajax(request=request):
            # Save the POST arguements
            data = json.load(request)

            sale_attributes = {
                "customer": Customer.objects.get(id=int(data['customer'])),
                "sub_total": float(data["sub_total"]),
                "grand_total": float(data["grand_total"]),
                "tax_amount": float(data["tax_amount"]),
                "tax_percentage": float(data["tax_percentage"]),
                "amount_payed": float(data["amount_payed"]),
                "amount_change": float(data["amount_change"]),
            }
            try:
                # Create the sale
                new_sale = Sale.objects.create(**sale_attributes)
                new_sale.save()
                # Create the sale details
                products = data["products"]

                for product in products:
                    detail_attributes = {
                        "sale": Sale.objects.get(id=new_sale.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "price": product["price"],
                        "weight": product['weight'],
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"]
                    }
                    sale_detail_new = SaleDetail.objects.create(
                        **detail_attributes)
                    sale_detail_new.save()

                print("Sale saved")

                messages.success(
                    request, 'Sale created succesfully!', extra_tags="success")

            except Exception as e:
                messages.success(
                    request, 'There was an error during the creation!', extra_tags="danger")

        return redirect('sales:sales_list')

    return render(request, "sales/sales_add.html", context=context)


@login_required(login_url="/accounts/login/")
def SalesDetailsView(request, sale_id):
    """
    Args:
        sale_id: ID of the sale to view
    """
    try:
        # Get tthe sale
        sale = Sale.objects.get(id=sale_id)

        # Get the sale details
        details = SaleDetail.objects.filter(sale=sale)

        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, 'There was an error getting the sale!', extra_tags="danger")
        print(e)
        return redirect('sales:sales_list')


@login_required(login_url="/accounts/login/")
def ReceiptPDFView(request, sale_id):
    """
    Args:
        sale_id: ID of the sale to view the receipt
    """
    # Get the sale
    sale = Sale.objects.get(id=sale_id)

    # Get the sale details
    details = SaleDetail.objects.filter(sale=sale)

    # Get the path to the image file
    image_path = finders.find('img/logo.png')

    # Read the image file and encode it as base64
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "details": details,
        "company_logo": encoded_image,  # Pass the encoded image to the context
    }
    html_template = template.render(context)

    # CSS Bootstrap
    css_url = os.path.join(settings.BASE_DIR, 'static/css/receipt_pdf/bootstrap.min.css')

    # Create the PDF
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")


def InvoicePDFView(request, sale_id):
    """
    Args:
        sale_id: ID of the sale to view the invoice
    """
    # Get the sale
    sale = Sale.objects.get(id=sale_id)

    # Get the sale details
    details = SaleDetail.objects.filter(sale=sale)

    # Get the path to the image file
    image_path = finders.find('img/logo.png')

    # Read the image file and encode it as base64
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    template = get_template("sales/sales_invoice_pdf.html")
    context = {
        "sale": sale,
        "details": details,
        "company_logo": encoded_image,  # Pass the encoded image to the context
    }
    html_template = template.render(context)

    # CSS Bootstrap
    css_url = os.path.join(settings.BASE_DIR, 'static/css/receipt_pdf/bootstrap.min.css')

    # Create the PDF
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")
