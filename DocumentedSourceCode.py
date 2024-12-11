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

import tkinter as tk  # Import tkinter for GUI development
from tkinter import messagebox, Toplevel  # Import specific tkinter modules for dialogs and popups
from PIL import Image, ImageTk  # Import Pillow for image handling
import csv  # Import CSV module for expense file handling
import matplotlib.pyplot as plt  # Import matplotlib for visualizations
import pandas as pd  # Import pandas for data processing
from datetime import datetime  # Import datetime for date validation

class EcoFriendlyBudgetTracker:
    """
    Main class for the Eco-Friendly Budget Tracker application.
    Handles GUI, data validation, and file processing.
    """
    def __init__(self, root):
        """
        Initializes the application, loads images, and starts the main dashboard.
        """
        self.root = root
        self.root.title("Eco-Friendly Budget Tracker")  # Set the title of the application window
        self.root.geometry("400x300")  # Set the window size

        # Variables to hold images
        self.leaf_image = None
        self.sun_image = None
        self.load_images()  # Load images used in the GUI

        # Display the main dashboard
        self.main_dashboard()

    def load_images(self):
        """
        Loads the images used in the application.
        """
        try:
            self.leaf_image = ImageTk.PhotoImage(Image.open("leaf.png").resize((100, 100)))  # Load leaf image
            self.sun_image = ImageTk.PhotoImage(Image.open("sun.jpeg").resize((100, 100)))  # Load sun image
        except Exception as e:
            # Handle errors in loading images
            self.leaf_image = None
            self.sun_image = None
            messagebox.showerror("Image Error", f"Error loading images: {e}")

    def main_dashboard(self):
        """
        Displays the main dashboard with navigation buttons.
        """
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear existing widgets

        if self.leaf_image:
            tk.Label(self.root, image=self.leaf_image).pack(pady=10)  # Display leaf image
        tk.Label(self.root, text="Eco-Friendly Budget Tracker", font=("Arial", 16)).pack(pady=10)  # App title

        # Navigation buttons
        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Eco Summary", command=self.eco_summary).pack(pady=5)
        tk.Button(self.root, text="Eco Tips", command=self.eco_goals).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=20)

    def add_expense(self):
        """
        Displays the add expense window for logging new expenses.
        """
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear existing widgets

        if self.sun_image:
            tk.Label(self.root, image=self.sun_image).pack(pady=10)  # Display sun image
        tk.Label(self.root, text="Log Your Expense", font=("Arial", 14)).pack(pady=10)

        # Input fields for expense details
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

        # Buttons for saving or returning to the dashboard
        tk.Button(self.root, text="Save Expense", command=lambda: self.save_expense(expense_name, amount, category, date)).pack(pady=10)
        tk.Button(self.root, text="Back to Main Dashboard", command=self.main_dashboard).pack()

    def save_expense(self, expense_name, amount, category, date):
        """
        Validates and saves the entered expense data to a CSV file.
        """
        if not expense_name.get() or not amount.get() or not category.get() or not date.get():
            messagebox.showerror("Validation Error", "All fields must be filled!")  # Check for empty fields
            return
        try:
            float(amount.get())  # Validate amount is numeric
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a number!")
            return
        if not self.validate_date(date.get()):
            messagebox.showerror("Validation Error", "Date must be in YYYY-MM-DD format!")  # Validate date format
            return

        # Save expense to CSV
        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense_name.get(), amount.get(), category.get(), date.get()])

        messagebox.showinfo("Success", "Expense saved successfully!")
        self.main_dashboard()

    def validate_date(self, date):
        """
        Validates the date format as YYYY-MM-DD.
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def eco_summary(self):
        """
        Generates and displays a pie chart summarizing expenses by category.
        """
        try:
            data = pd.read_csv("expenses.csv", header=None, names=["Name", "Amount", "Category", "Date"])  # Read expense data
        except FileNotFoundError:
            messagebox.showerror("Error", "No expenses found! Please add some first.")  # Handle missing file
            return

        data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")  # Ensure numeric amounts
        category_totals = data.groupby("Category")["Amount"].sum()  # Group data by category

        plt.figure(figsize=(6, 6))  # Create pie chart
        plt.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
        plt.title("Spending Breakdown by Category")
        plt.show()

    def eco_goals(self):
        """
        Displays eco-friendly budgeting tips in a popup window.
        """
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


if __name__ == "__main__":
    root = tk.Tk()
    app = EcoFriendlyBudgetTracker(root)
    root.mainloop()
