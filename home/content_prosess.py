

from django.shortcuts import render
 
def canvass(request):
  monthly_expense_data = [
    { "label": "Accomodation", "y": 30 },
    { "label": "Food & Groceries", "y": 25 },
    { "label": "Utilities", "y": 5 },
    { "label": "Entertainment & Fun", "y": 20 },
    { "label": "Savings", "y": 10 },
    { "label": "Cellphone & Internet", "y": 10 }
  ]
 
  return  { "monthly_expense_data" : monthly_expense_data }



def order(request):
  orders = [
    { "id": 1, "customer": "John Doe", "status": "Pending", "total_amount": 100 },
    { "id": 2, "customer": "Jane Smith", "status": "Completed", "total_amount": 500 },
    { "id": 3, "customer": "Michael Johnson", "status": "Canceled", "total_amount": 200 }
  ]
  return  { "orders" : orders }