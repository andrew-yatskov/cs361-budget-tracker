from storage import load_expenses, save_expenses
from datetime import date, datetime
import time

CATEGORIES = ["Food", "Transportation", "Shopping", "Bills", "Entertainment", "Other"]


def show_main_menu():
    print(
        "*" * 54,
        "\n",
        "BUDGET TRACKER".center(54),
        "\n",
        "*" * 54,
    """
    Log your spending and see exactly where your money
    goes, so you can stay on budget.
    Your expenses are saved only on this computer
    (expenses.json). No account or internet needed.
    """,
        "\nMAIN MENU",
    """
    1. Add an expense (takes about 30 seconds)
    2. View my expenses
    3. Delete an expense
    H. Help - how each option works (optional)
    0. Quit
    """
    )


def ask(prompt):
    """Gets input from the user. Returns "B" or "X" if they typed back or cancel."""
    answer = input(prompt).strip()
    if answer.upper() in ("B", "X"):
        return answer.upper()
    return answer


def print_table(items):
    """Prints expenses in the same table layout used by View and Delete."""
    print(f"{'#':>2}  {'Date':<10}  {'Category':<14}  {'Amount':>9}  Note")
    for number, item in enumerate(items, start=1):
        print(f"{number:>2}  {item['date']:<10}  {item['category']:<14}  "
              f"${item['amount']:>8.2f}  {item['note']}")


def add_expense(expenses):
    temp_amount = None
    temp_category = None
    temp_date = None
    temp_note = None
    user_dict = {}

    print(
        "ADD AN EXPENSE".center(54),
        "\n",
        "-" * 54,
    """
    You'll enter 4 things: 1) Amount 2) Category
    3) Date 4) Note. Then you review before saving.
    Type B to go back a step or X to cancel anytime.
    """
    )

    step = 1
    while True:
        # Step 1 - Amount
        if step == 1:
            print("\nStep 1 of 4 - Amount in dollars (example: 12.50)")
            answer = ask("Enter amount: ")
            if answer in ("B", "X"):
                print("\nCancelled. Nothing was saved.")
                input("Press Enter to return to the Main Menu.")
                return
            try:
                temp_amount = float(answer)
            except ValueError:
                print("Amount must be a number greater than 0. Try again.")
                continue
            if temp_amount <= 0:
                print("Amount must be a number greater than 0. Try again.")
                continue
            temp_amount = round(temp_amount, 2)
            step = 2

        # Step 2 - Category (user enters a number)
        elif step == 2:
            print(
                """
        Step 2 of 4 - Category (enter a number)
        1. Food
        2. Transportation
        3. Shopping
        4. Bills
        5. Entertainment
        6. Other
        """
            )
            answer = ask("Enter Category: ")
            if answer == "X":
                print("\nCancelled. Nothing was saved.")
                input("Press Enter to return to the Main Menu.")
                return
            if answer == "B":
                step = 1
                continue
            if answer.isdigit() and 1 <= int(answer) <= len(CATEGORIES):
                temp_category = CATEGORIES[int(answer) - 1]
                step = 3
            else:
                print("Please enter a number from 1 to 6.")

        # Step 3 - Date (Enter = today)
        elif step == 3:
            today = date.today().isoformat()
            print(f"\nStep 3 of 4 - Date as YYYY-MM-DD, or press Enter for today ({today})")
            answer = ask("Enter Date: ")
            if answer == "X":
                print("\nCancelled. Nothing was saved.")
                input("Press Enter to return to the Main Menu.")
                return
            if answer == "B":
                step = 2
                continue
            if answer == "":
                temp_date = today
                step = 4
                continue
            try:
                datetime.strptime(answer, "%Y-%m-%d")
            except ValueError:
                print(f"Date must look like YYYY-MM-DD (example: {today}). Try again.")
                continue
            temp_date = answer
            step = 4

        # Step 4 - Note
        elif step == 4:
            print("\nStep 4 of 4 - Short note (example: Lunch at Panda)")
            answer = ask("Enter Note: ")
            if answer == "X":
                print("\nCancelled. Nothing was saved.")
                input("Press Enter to return to the Main Menu.")
                return
            if answer == "B":
                step = 3
                continue
            if answer == "":
                print("Please type a short note so you can find this expense later.")
                continue
            temp_note = answer
            step = 5

        # Review & Save
        else:
            print("\n", "REVIEW YOUR EXPENSE".center(54), "\n", "-" * 54)
            print(
                f"""
           Amount:   ${temp_amount:.2f}
           Category: {temp_category}
           Date:     {temp_date}
           Note:     {temp_note}

           Save this expense?
           Y = Save it
           B = Go back and change a step
           X = Cancel (nothing will be saved)
        """
            )
            answer = ask("> ").upper()
            if answer == "Y":
                user_dict.update({"amount": temp_amount, "category": temp_category,
                                  "date": temp_date, "note": temp_note})
                expenses.insert(0, user_dict)
                save_expenses(expenses)
                print(f"\nSaved! {temp_note} - ${temp_amount:.2f} ({temp_category}, {temp_date})")
                print(f"You now have {len(expenses)} expenses.")
                input("\nPress Enter to return to the Main Menu.")
                return
            elif answer == "B":
                step = 4
            elif answer == "X":
                print("\nCancelled. Nothing was saved.")
                input("Press Enter to return to the Main Menu.")
                return
            else:
                print("Please type Y, B, or X.")


def view_expenses(expenses):
    if not expenses:
        print("\nMY EXPENSES\n", "-" * 54)
        print(
            """
            You haven't added any expenses yet.
            To add your first one, go back to the Main Menu
            and choose 1. Add an expense. It takes about
            30 seconds.
            """
            )
        input("Press Enter to return to the Main Menu.")
        return

    start = time.perf_counter()
    total = 0
    num_expenses = len(expenses)
    print("\nMY EXPENSES (newest first)\n", "-" * 54)
    print_table(expenses)
    for i in expenses:
        total += i["amount"]
    print("-" * 54)
    print(f"Total spent: ${total:.2f}   ({num_expenses} expenses)")
    elapsed = time.perf_counter() - start
    print(f"(List shown in {elapsed:.3f} seconds)")
    input("\nPress Enter to return to the Main Menu.")


def search_expense(expenses):
    """Lets the user find an expense by a word in its note.
    Returns the chosen expense, None to go back to the full list, or "X" to cancel."""
    while True:
        print("\n", "SEARCH FOR AN EXPENSE TO DELETE".center(54), "\n", "-" * 54)
        word = ask("Type a word from the note (example: gas): ")
        if word == "B":
            return None
        if word == "X":
            return "X"
        if word == "":
            print("Please type a word to search for.")
            continue

        matches = [i for i in expenses if word.lower() in i["note"].lower()]
        if not matches:
            print(f'\nNo expenses have "{word}" in the note. Try another word, or type B to go back.')
            continue

        print(f"\nFound {len(matches)} match(es):")
        print_table(matches)
        while True:
            answer = ask("\nEnter the # to delete, S to search again,\nor B to go back to the full list: ")
            if answer == "B":
                return None
            if answer == "X":
                return "X"
            if answer.upper() == "S":
                break
            if answer.isdigit() and 1 <= int(answer) <= len(matches):
                return matches[int(answer) - 1]
            print(f"Please enter a number from 1 to {len(matches)}, S, or B.")


def confirm_delete(expenses, item):
    """Asks Y/N before deleting. Returns True if it was deleted."""
    print("\n", "CONFIRM DELETE".center(54), "\n", "-" * 54)
    print("You are about to delete:")
    print(f'  {item["date"]}  {item["category"]}  ${item["amount"]:.2f}  "{item["note"]}"')
    print("\nWarning: a deleted expense cannot be recovered.")
    print("Type Y to delete it, or N to keep it and go back.")
    while True:
        answer = input("> ").strip().upper()
        if answer == "Y":
            expenses.remove(item)
            save_expenses(expenses)
            print(f'\nDeleted "{item["note"]}" - ${item["amount"]:.2f}.')
            print(f"You now have {len(expenses)} expenses.")
            input("\nPress Enter to return to the Main Menu.")
            return True
        if answer == "N":
            print("\nKept it. Nothing was deleted.")
            return False
        print("Please type Y to delete or N to keep it.")


def delete_expense(expenses):
    if not expenses:
        print("\nDELETE AN EXPENSE\n", "-" * 54)
        print(
            """
            You don't have any expenses to delete yet.
            To add one, go back to the Main Menu and
            choose 1. Add an expense.
            """
        )
        input("Press Enter to return to the Main Menu.")
        return

    while True:
        print("\n", "DELETE AN EXPENSE".center(54), "\n", "-" * 54)
        print_table(expenses)
        print("-" * 54)
        print(
            """Enter the # of the expense you want to delete.
Can't find it? Type S to search by a word in its
note instead.
Type B to go back to the Main Menu."""
        )
        answer = ask("> ")
        if answer in ("B", "X"):
            return

        if answer.upper() == "S":
            chosen = search_expense(expenses)
            if chosen is None:
                continue
            if chosen == "X":
                return
        elif answer.isdigit() and 1 <= int(answer) <= len(expenses):
            chosen = expenses[int(answer) - 1]
        else:
            print(f"Please enter a number from 1 to {len(expenses)}, S, or B.")
            continue

        if confirm_delete(expenses, chosen):
            return


def show_help():
    print(
        "\n",
        "HELP - HOW BUDGET TRACKER WORKS".center(54),
        "\n",
        "-" * 54,
        """
        1. Add an expense
        Answer 4 short prompts: amount, category, date,
        and note. Nothing is saved until you confirm.

        2. View my expenses
        Shows every expense, newest first, plus the
        total you have spent.

        3. Delete an expense
        Pick an expense by its # in the list, or search
        for it by a word in its note. You will always
        be asked to confirm before anything is deleted.

        Tip: At any prompt, type B to go back one step or
        X to cancel and return to the Main Menu.
        """
    )
    input("Press Enter to return to the Main Menu.")


def main():
    expenses = load_expenses()
    while True:
        show_main_menu()
        choice = input("Choose an option and press Enter: ").strip().upper()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "H":
            show_help()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, H, or 0.")


if __name__ == "__main__":
    main()