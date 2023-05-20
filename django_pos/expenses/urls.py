from django.urls import path

from . import views

app_name = "expenses"
urlpatterns = [
    # List groups
    path('groups', views.GroupsListView, name='groups_list'),
    # Add group
    path('groups/add', views.GroupsAddView, name='groups_add'),
    # Update group
    path('groups/update/<str:group_id>',
         views.GroupsUpdateView, name='groups_update'),
    # Delete group
    path('groups/delete/<str:group_id>',
         views.GroupsDeleteView, name='groups_delete'),

    # List expenses
    path('', views.ExpensesListView, name='expenses_list'),
    # Add expense
    path('add', views.ExpensesAddView, name='expenses_add'),
    # Update expense
    path('update/<str:expense_id>',
         views.ExpensesUpdateView, name='expenses_update'),
    # Delete expense
    path('delete/<str:expense_id>',
         views.ExpensesDeleteView, name='expenses_delete'),
    # Get expenses AJAX
    path("get", views.GetExpensesAJAXView, name="get_expenses"),

     # List capitals
    path('capitals', views.CapitalsListView, name='capitals_list'),
    # Add capital
    path('capitals/add', views.CapitalsAddView, name='capitals_add'),
    # Update capital
    path('capitals/update/<str:capital_id>',
         views.CapitalsUpdateView, name='capitals_update'),
    # Delete capital
    path('capitals/delete/<str:capital_id>',
         views.CapitalsDeleteView, name='capitals_delete'),


]