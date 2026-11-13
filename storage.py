import json
import os

EXPENSES_FILE = "expenses.json"
TEMP_FILE = "expenses.tmp"

def load_expenses(): 
    if not os.path.exists(EXPENSES_FILE):
        return []
    with open(EXPENSES_FILE, "r") as file:
        return json.load(file)

def save_expenses(expenses):
    with open(TEMP_FILE, "w") as file:
        json.dump(expenses, file, indent = 2)
    os.replace(TEMP_FILE, EXPENSES_FILE)


#test_list = [{"amount": 14.75, "category": "Food", "date": "2026-11-07", "note": "Ramen"}]
#save_expenses(test_list)
#print(load_expenses())
