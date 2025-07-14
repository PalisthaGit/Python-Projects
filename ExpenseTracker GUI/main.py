import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import sqlite3

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT
    )
''')

def setup_treeview(tree, columns):
    for col in columns:
        tree.heading(col, text=col.capitalize())
        if col == "description":
            tree.column(col, width=160)
        elif col == "amount":
            tree.column(col, width=70)
        else:
            tree.column(col, width=100)

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
columns = ("id", "amount", "date", "category", "description")

notebook = ttk.Notebook(root)
notebook.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
daily_frame = ttk.Frame(notebook)
monthly_frame = ttk.Frame(notebook)
yearly_frame = ttk.Frame(notebook)
custom_frame = ttk.Frame(notebook)

notebook.add(daily_frame, text="Daily")
notebook.add(monthly_frame, text="Monthly")
notebook.add(yearly_frame, text="Yearly")
notebook.add(custom_frame, text="Custom Search")

# --- Table in Daily Tab ---
daily_tree = ttk.Treeview(daily_frame, columns=columns, show="headings", height=12)
setup_treeview(daily_tree, columns)
daily_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
today_label = tk.Label(daily_frame, text="Daily Expenses", font=("Arial", 12, "bold"))
today_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# --- Table in Monthly Tab ---
monthly_tree = ttk.Treeview(monthly_frame, columns=columns, show="headings", height=10)
setup_treeview(monthly_tree, columns)
monthly_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
monthly_label = tk.Label(monthly_frame, text="Monthly Expenses", font=("Arial", 12, "bold"))
monthly_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# --- Table in Yearly Tab ---
yearly_tree = ttk.Treeview(yearly_frame, columns=columns, show="headings", height=10)
setup_treeview(yearly_tree, columns)
yearly_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
yearly_label = tk.Label(yearly_frame, text="Yearly Expenses", font=("Arial", 12, "bold"))
yearly_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# --- Custom Tab ---
from_label = tk.Label(custom_frame, text="From:")
from_label.grid(row=0, column=0, padx=5, pady=5)
from_date = DateEntry(custom_frame, date_pattern="yyyy-mm-dd", maxdate=date.today())
from_date.grid(row=0, column=1, padx=5, pady=5)

to_label = tk.Label(custom_frame, text="To:")
to_label.grid(row=0, column=2, padx=5, pady=5)
to_date = DateEntry(custom_frame, date_pattern="yyyy-mm-dd", maxdate=date.today())
to_date.grid(row=0, column=3, padx=5, pady=5)

search_btn = tk.Button(custom_frame, text="Search")
search_btn.grid(row=0, column=4, padx=5, pady=5)

custom_tree = ttk.Treeview(custom_frame, columns=columns, show="headings", height=12)
setup_treeview(custom_tree, columns)
custom_tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

custom_total_var = tk.StringVar()
custom_total_label = tk.Label(custom_frame, textvariable=custom_total_var, font=("Arial", 12, "bold"))
custom_total_label.grid(row=2, column=0, columnspan=5, sticky="w", padx=10, pady=(0, 10))

# --- Add Expense Form ---
amount_label = tk.Label(root, text="Amount")
amount_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

date_label = tk.Label(root, text="Date (YYYY-MM-DD)")
date_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
date_entry = DateEntry(root, date_pattern="yyyy-mm-dd", maxdate=date.today())
date_entry.grid(row=0, column=3, padx=5, pady=5)

category_label = tk.Label(root, text="Category")
category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
category_options = ["food", "travel", "groceries", "entertainment"]
category_var = tk.StringVar(value=category_options[0])
category_menu = ttk.Combobox(root, textvariable=category_var, values=category_options, state="readonly")
category_menu.grid(row=1, column=1, padx=5, pady=5)

desc_label = tk.Label(root, text="Description")
desc_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
desc_entry = tk.Entry(root)
desc_entry.grid(row=1, column=3, padx=5, pady=5)

# --- Total label ---
total_var = tk.StringVar()
total_label = tk.Label(root, textvariable=total_var, font=("Arial", 12, "bold"))
total_label.grid(row=4, column=0, columnspan=6, sticky="w", padx=10, pady=(0, 10))

# --- Load daily expenses function ---
def load_daily():
    for row in daily_tree.get_children():
        daily_tree.delete(row)
    today = date.today().isoformat()
    cur.execute("SELECT id, amount, date, category, description FROM expenses WHERE date = ?", (today,))
    for row in cur.fetchall():
        daily_tree.insert("", tk.END, values=row)
    # Total for today
    cur.execute("SELECT SUM(amount) FROM expenses WHERE date = ?", (today,))
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    total_var.set(f"Today's Total: ₹ {total:.2f}")

# --- Load monthly expenses function ---
def load_monthly():
    for row in monthly_tree.get_children():
        monthly_tree.delete(row)
    this_month = date.today().strftime("%Y-%m")
    cur.execute("SELECT id, amount, date, category, description FROM expenses WHERE date LIKE ?", (this_month+'%',))
    for row in cur.fetchall():
        monthly_tree.insert("", tk.END, values=row)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (this_month + '%',))
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    total_var.set(f"This Month's Total: ₹ {total:.2f}")

# --- Load yearly expenses function ---
def load_yearly():
    for row in yearly_tree.get_children():
        yearly_tree.delete(row)
    this_year = date.today().strftime("%Y")
    cur.execute("SELECT id, amount, date, category, description FROM expenses WHERE date LIKE ?", (this_year+'%',))
    for row in cur.fetchall():
        yearly_tree.insert("", tk.END, values=row)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (this_year + '%',))
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    total_var.set(f"This Year's Total: ₹ {total:.2f}")

# --- Add expense function ---
def add_expense():
    amount = amount_entry.get()
    try:
        amount_input = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount field (e.g., 12.50).")
        return
    if amount_input <= 0:
        messagebox.showerror("Invalid Amount", "Amount should be greater than 0. Please enter a positive number.")
        return

    date_value = date_entry.get()
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter date in format eg: 2029-09-07")
        return

    category = category_var.get()
    if category not in category_options:
        messagebox.showerror("Invalid Category", "Please select a valid category from the list.")
        return

    description = desc_entry.get()
    if len(description) > 100:
        messagebox.showerror("Description Too Long", "Description should be 100 characters or less.")
        return

    cur.execute(
        "INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)",
        (amount_input, date_value, category, description)
    )
    conn.commit()
    messagebox.showinfo("Expense Added", "Expense added successfully!")

    # Clear fields
    amount_entry.delete(0, tk.END)
    date_entry.set_date(date.today())
    desc_entry.delete(0, tk.END)
    category_var.set(category_options[0])

    # Refresh the table and total for current tab
    selected_tab = notebook.tab(notebook.index("current"))["text"]
    if selected_tab == "Daily":
        load_daily()
    elif selected_tab == "Monthly":
        load_monthly()
    elif selected_tab == "Yearly":
        load_yearly()
    elif selected_tab == "Custom Search":
        for row in custom_tree.get_children():
            custom_tree.delete(row)
        custom_total_var.set("")
        total_var.set("")

# --- Search expenses function for Custom Tab ---
def search_expenses():
    # Get the selected dates
    from_date_val = from_date.get()
    to_date_val = to_date.get()

    # Validate date order
    if from_date_val > to_date_val:
        messagebox.showerror("Invalid Dates", "From date cannot be after To date!")
        return

    # Clear previous results
    for row in custom_tree.get_children():
        custom_tree.delete(row)

    # Fetch from DB
    cur.execute("""
        SELECT id, amount, date, category, description FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY date ASC
    """, (from_date_val, to_date_val))
    results = cur.fetchall()
    for row in results:
        custom_tree.insert("", tk.END, values=row)

    # Show total
    cur.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (from_date_val, to_date_val))
    total = cur.fetchone()[0]
    if total is None:
        total = 0
    custom_total_var.set(f"Total: ₹ {total:.2f}")

# Attach the search function to the button
search_btn.config(command=search_expenses)

# --- Tab change event ---
def on_tab_changed(event):
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]
    if selected_tab == "Daily":
        load_daily()
    elif selected_tab == "Monthly":
        load_monthly()
    elif selected_tab == "Yearly":
        load_yearly()
    elif selected_tab == "Custom Search":
        # Clear results when switching to this tab
        for row in custom_tree.get_children():
            custom_tree.delete(row)
        custom_total_var.set("")
        total_var.set("")  # <-- clears the main total label

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# --- Add Button ---
add_btn = tk.Button(root, text="Add Expense", command=add_expense)
add_btn.grid(row=0, column=5, rowspan=2, padx=10, pady=5, sticky="ns")

# --- Load today's data on start ---
load_daily()

# --- Close DB connection on window close ---
def on_closing():
    conn.close()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
