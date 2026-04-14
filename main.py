import tkinter as tk
from tkinter import ttk
from database import create_tables
from suppliers_view import SuppliersView

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Company Purchase and Expense Tracking System")
        self.geometry("1000x600")
        self.minsize(900, 500)

        create_tables()

        title_label = tk.Label(
            self,
            text="Company Purchase and Expense Tracking System",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        suppliers_tab = SuppliersView(notebook)
        purchases_tab = ttk.Frame(notebook)
        expenses_tab = ttk.Frame(notebook)
        dashboard_tab = ttk.Frame(notebook)
        reports_tab = ttk.Frame(notebook)

        notebook.add(dashboard_tab, text="Dashboard")
        notebook.add(suppliers_tab, text="Suppliers")
        notebook.add(purchases_tab, text="Purchases")
        notebook.add(expenses_tab, text="Expenses")
        notebook.add(reports_tab, text="Reports")

        self.build_placeholder(dashboard_tab, "Dashboard view coming soon...")
        self.build_placeholder(purchases_tab, "Purchases view coming soon...")
        self.build_placeholder(expenses_tab, "Expenses view coming soon...")
        self.build_placeholder(reports_tab, "Reports view coming soon...")

    def build_placeholder(self, parent, text):
        label = tk.Label(parent, text=text, font=("Arial", 14))
        label.pack(expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()