import tkinter as tk
from tkinter import ttk, messagebox
from models import add_supplier, get_suppliers

class SuppliersView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form_frame = ttk.LabelFrame(self, text="Add Supplier")
        form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ttk.Label(form_frame, text="Company Name:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.company_name_entry = ttk.Entry(form_frame, width=35)
        self.company_name_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.phone_entry = ttk.Entry(form_frame, width=35)
        self.phone_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.email_entry = ttk.Entry(form_frame, width=35)
        self.email_entry.grid(row=2, column=1, padx=8, pady=8)

        add_button = ttk.Button(form_frame, text="Save Supplier", command=self.save_supplier)
        add_button.grid(row=3, column=0, padx=8, pady=10)

        refresh_button = ttk.Button(form_frame, text="Refresh Table", command=self.load_suppliers)
        refresh_button.grid(row=3, column=1, padx=8, pady=10, sticky="w")

        table_frame = ttk.LabelFrame(self, text="Suppliers List")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Company", "Phone", "Email"),
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Company", text="Company Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Company", width=250)
        self.tree.column("Phone", width=180)
        self.tree.column("Email", width=250)

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        self.load_suppliers()

    def save_supplier(self):
        company_name = self.company_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not company_name:
            messagebox.showerror("Error", "Company name is required.")
            return

        try:
            add_supplier(company_name, phone, email)
            messagebox.showinfo("Success", "Supplier saved successfully.")
            self.clear_form()
            self.load_suppliers()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save supplier:\n{e}")

    def load_suppliers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            suppliers = get_suppliers()
            for supplier in suppliers:
                self.tree.insert("", "end", values=supplier)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load suppliers:\n{e}")

    def clear_form(self):
        self.company_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)