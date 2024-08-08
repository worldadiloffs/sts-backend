

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