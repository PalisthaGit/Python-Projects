import sqlite3
from datetime import date, datetime

conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

allowed_categories = ["food", "travel", "groceries", "entertainment"]

cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT
    )
''')

sample_data = [
    (40.0, '2025-04-20', 'groceries', 'Vegetables'),
    (25.0, '2025-05-02', 'food', 'Dinner'),
    (18.0, '2025-05-15', 'entertainment', 'Movie'),
    (30.0, '2025-05-28', 'groceries', 'Snacks'),
    (22.0, '2025-06-05', 'food', 'Breakfast'),
    (17.5, '2025-06-18', 'travel', 'Taxi'),
    (35.0, '2025-06-25', 'groceries', 'Fruits'),
]
for data in sample_data:
    cur.execute("INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)", data)


def add_expense():
    while True:
        amount_input = input("Enter the amount: ")
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount should be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a number.")

    while True:
        expense_date = input("Enter the date (YYYY-MM-DD) [Press Enter for today]: ").strip()
        if expense_date == "":
            expense_date = date.today().isoformat()
            break
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Please enter a valid date format (2025-06-26) or press Enter for today.")

    while True:
        category = input(f"Enter the category ({', '.join(allowed_categories)}): ").strip().lower()
        if category not in allowed_categories:
            print("Please choose a category from the list.")
        else:
            break

    description = input("Enter a description: ")

    cur.execute(
        "INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)",
        (amount, expense_date, category, description)
    )
    conn.commit()
    print("Expense added.")

def view_expenses():
    cur.execute('SELECT * FROM expenses')
    rows = cur.fetchall()
    if not rows:
        print("No expenses found")
    else:
        print(f"{'ID':<4} {'Amount':<8} {'Date':<12} {'Category':<15} {'Description':<20}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<8} {row[2]:<12} {row[3]:<15} {row[4]:<20}")   
        cur.execute("SELECT SUM(amount) FROM expenses")
        total_amount = cur.fetchone()[0]
        if total_amount is None:
            total_amount = 0
        print("-"*60)
        print(f"{'Total: ':<10}{total_amount:<8}") 

def show_total_expenses():
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    print("Total expense so far: $", total)

def show_today_expenses():
    today = date.today().isoformat()
    cur.execute("SELECT * FROM expenses WHERE date = ?", (today,))
    rows = cur.fetchall()
    if not rows:
        print("No expenses today")
    else:
        print(f"{'ID':<4} {'Amount':<8} {'Date':<12} {'Category':<15} {'Description':<20}")
        print("-"*60)
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<8} {row[2]:<12} {row[3]:<15} {row[4]:<20}")
        cur.execute("SELECT SUM(amount) FROM expenses WHERE date = ?", (today,))
        total_today = cur.fetchone()[0]
        if total_today is None:
            total_today = 0
        print("-"* 60)
        print(f"{'Total Today':<15} {total_today:<8}")

def show_current_month_expenses():
    current_month = date.today().isoformat()[:7]
    cur.execute("SELECT * FROM expenses WHERE date LIKE ?", (current_month + '%',))
    rows = cur.fetchall()
    if not rows:
        print("No expenses current month")
    else:
        print(f"{'ID':<4} {'Amount':<8} {'Date':<12} {'Category':<15} {'Description':<20}")
        print("-"*60)
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<8} {row[2]:<12} {row[3]:<15} {row[4]:<20}")
        cur.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (current_month + '%',))
        monthly_total = cur.fetchone()[0]
        if monthly_total is None:
            monthly_total = 0
        print("-"*60)
        print(f"{'Total this month: ':<15}{monthly_total :<8}")

def show_selected_month_expenses():
    selected_month = input("Enter the month you want to see (YYYY-MM): ")
    cur.execute("SELECT * FROM expenses WHERE date LIKE ?", (selected_month + '%',))
    rows = cur.fetchall()
    if not rows:
        print("No expense in selected month")
    else:
        print(f"{'ID':<4} {'Amount':<8} {'Date':<12} {'Category':<15} {'Description':<20}")
        print("-"*60)
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<8} {row[2]:<12} {row[3]:<15} {row[4]:<20}")  
        cur.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (selected_month + '%',))
        selected_total = cur.fetchone()[0]
        if selected_total is None:
            selected_total = 0
        print("-" * 60)
        print(f"Total expenses for {selected_month}: $ {selected_total}")


while True:
    print("\nWhat do you want to do?")
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. Show today's total expense")
    print("4. Show current month's total")
    print("5. Show total expense for a selected month")
    print("6. Exit")
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_today_expenses()
    elif choice == "4":
        show_current_month_expenses()
    elif choice == "5":
        show_selected_month_expenses()
    elif choice == "6":
        print("Okay, exited")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 7.")

conn.commit()
conn.close()
