from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, FloatField, F, IntegerField, DateField, Avg
from django.db.models.functions import Coalesce, TruncDate, TruncDay, TruncWeek, TruncMonth
from django.shortcuts import render
from products.models import Product, Category
from purchases.models import Purchase, PurchaseDetail
from sales.models import Sale, SaleDetail
import json


@login_required(login_url="/accounts/login/")
def index(request):
    today = date.today()

    year = today.year
    monthly_earnings = []

    # Caculate earnings per month
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings)/12, '.2f')

    # Top selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    print(top_products_names)
    print(top_products_quantity)

    total_revenue = Sale.objects.aggregate(total_revenue=Sum('grand_total'))['total_revenue']
    
    total_sales_count = Sale.objects.count()
    average_revenue_per_sale = round(total_revenue / total_sales_count, 2)
    total_quantity_sold = SaleDetail.objects.aggregate(total_quantity_sold=Sum('quantity'))['total_quantity_sold']
    
    top_selling_products = SaleDetail.objects.values('product__name').annotate(quantity_sold=Sum('quantity')).order_by('-quantity_sold')[:5]
    sales_by_category = SaleDetail.objects.values('product__category__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')
    daily_sales_trend = Sale.objects.annotate(date=TruncDate('date_added')).values('date').annotate(daily_revenue=Sum('grand_total')).order_by('date')


    # Total number of purchases
    total_purchases = Purchase.objects.count()

    # Total purchase amount
    total_purchase_amount = Purchase.objects.aggregate(total_amount=Sum('grand_total'))['total_amount']

    # Average purchase amount
    avg_purchase_amount = round(Purchase.objects.aggregate(avg_amount=Avg('grand_total'))['avg_amount'], 2)

    # Total quantity of items purchased
    total_quantity_purchased = PurchaseDetail.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']

    # Total weight of items purchased
    total_weight_purchased = PurchaseDetail.objects.aggregate(total_weight=Sum('weight'))['total_weight']


    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "monthly_earnings": monthly_earnings,

        "avg_month": avg_month,

        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
        "top_selling_products": top_selling_products,
        "sales_by_category": sales_by_category,
        "daily_sales_trend": daily_sales_trend,
        "average_revenue_per_sale": average_revenue_per_sale,
        "total_quantity_sold": total_quantity_sold,

         # Include purchase summary data
        "total_purchases": total_purchases,
        "total_purchase_amount": total_purchase_amount,
        "avg_purchase_amount": avg_purchase_amount,
        "total_quantity_purchased": total_quantity_purchased,
        "total_weight_purchased": total_weight_purchased,

    }
    return render(request, "pos/index.html", context)

