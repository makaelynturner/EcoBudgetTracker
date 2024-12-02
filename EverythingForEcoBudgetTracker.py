"""
Eco-Friendly Budget Tracker
A Python tkinter GUI application to track expenses with a focus on sustainability.

Features:
- Add and log expenses with categories.
- View a summary of spending with visualizations.
- Receive eco-friendly budgeting tips.

Developed by: Makaelyn Turner
Date: December 2024
"""

import tkinter as tk
from tkinter import messagebox, Toplevel
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class EcoFriendlyBudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Eco-Friendly Budget Tracker")
        self.root.geometry("400x300")
        
        # Initialize Main Dashboard
        self.main_dashboard()

    # Main Dashboard
    def main_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Eco-Friendly Budget Tracker", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Eco Summary", command=self.eco_summary).pack(pady=5)
        tk.Button(self.root, text="Eco Tips", command=self.eco_goals).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=20)

    # Add Expense Window
    def add_expense(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Log Your Expense", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Expense Name:").pack()
        expense_name = tk.Entry(self.root)
        expense_name.pack()

        tk.Label(self.root, text="Amount:").pack()
        amount = tk.Entry(self.root)
        amount.pack()

        tk.Label(self.root, text="Category:").pack()
        category = tk.Entry(self.root)
        category.pack()

        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack()
        date = tk.Entry(self.root)
        date.pack()

        tk.Button(self.root, text="Save Expense", command=lambda: self.save_expense(expense_name, amount, category, date)).pack(pady=10)
        tk.Button(self.root, text="Back to Main Dashboard", command=self.main_dashboard).pack()

    def save_expense(self, expense_name, amount, category, date):
        if not expense_name.get() or not amount.get() or not category.get() or not date.get():
            messagebox.showerror("Validation Error", "All fields must be filled!")
            return
        try:
            float(amount.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a number!")
            return
        if not self.validate_date(date.get()):
            messagebox.showerror("Validation Error", "Date must be in YYYY-MM-DD format!")
            return

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense_name.get(), amount.get(), category.get(), date.get()])

        messagebox.showinfo("Success", "Expense saved successfully!")
        self.main_dashboard()

    def validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Eco Summary with Charts
    def eco_summary(self):
        try:
            data = pd.read_csv("expenses.csv", header=None, names=["Name", "Amount", "Category", "Date"])
        except FileNotFoundError:
            messagebox.showerror("Error", "No expenses found! Please add some first.")
            return

        data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")
        category_totals = data.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(6, 6))
        plt.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
        plt.title("Spending Breakdown by Category")
        plt.show()

    # Eco Tips Pop-Up
    def eco_goals(self):
        tips_window = Toplevel(self.root)
        tips_window.title("Eco Tips")
        tips_window.geometry("300x200")

        tips = [
            "1. Buy locally-produced goods.",
            "2. Use reusable bags and bottles.",
            "3. Opt for energy-efficient appliances.",
            "4. Avoid single-use plastics.",
            "5. Shop second-hand when possible."
        ]
        tk.Label(tips_window, text="Sustainable Budgeting Tips:", font=("Arial", 12)).pack(pady=10)
        for tip in tips:
            tk.Label(tips_window, text=tip, wraplength=250, justify="left").pack(anchor="w", padx=10)

        tk.Button(tips_window, text="Close", command=tips_window.destroy).pack(pady=10)


# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = EcoFriendlyBudgetTracker(root)
    root.mainloop()
