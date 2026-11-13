# Creates 100 fake expenses so you can show the
# "100 expenses in under 1 second" requirement.
# WARNING: this replaces whatever is in expenses.json.
import random
from storage import save_expenses

CATEGORIES = ["Food", "Transportation", "Shopping", "Bills", "Entertainment", "Other"]
NOTES = ["Lunch", "Gas", "Groceries", "Phone bill", "Movie", "Coffee", "Gym", "Books"]

expenses = []
for day in range(100):
    expenses.append({
        "amount": round(random.uniform(3, 80), 2),
        "category": random.choice(CATEGORIES),
        "date": f"2026-{random.randint(1, 11):02d}-{random.randint(1, 28):02d}",
        "note": random.choice(NOTES),
    })

save_expenses(expenses)
print("Saved 100 test expenses to expenses.json")