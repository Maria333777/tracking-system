import flet as ft
from models import add_expense, get_expenses

def expenses_view(page: ft.Page):
    category = ft.Dropdown(
        label="Category",
        width=200,
        options=[
            ft.dropdown.Option("Office Supplies"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("Maintenance"),
            ft.dropdown.Option("Utilities"),
            ft.dropdown.Option("Other"),
        ]
    )

    description = ft.TextField(label="Description", width=250)
    amount = ft.TextField(label="Amount", width=150)
    expense_date = ft.TextField(label="Expense Date (YYYY-MM-DD)", width=220)

    payment_method = ft.Dropdown(
        label="Payment Method",
        width=180,
        options=[
            ft.dropdown.Option("Cash"),
            ft.dropdown.Option("Card"),
            ft.dropdown.Option("Transfer"),
        ]
    )

    status = ft.Dropdown(
        label="Status",
        width=150,
        options=[
            ft.dropdown.Option("Paid"),
            ft.dropdown.Option("Pending"),
            ft.dropdown.Option("Approved"),
        ]
    )

    table_area = ft.Column()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def load_expenses():
        table_area.controls.clear()

        try:
            expenses_list = get_expenses()

            if not expenses_list:
                table_area.controls.append(ft.Text("No expenses saved yet."))
            else:
                rows = []
                for expense in expenses_list:
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(expense[0]))),
                                ft.DataCell(ft.Text(str(expense[1]))),
                                ft.DataCell(ft.Text(str(expense[2]))),
                                ft.DataCell(ft.Text(str(expense[3]))),
                                ft.DataCell(ft.Text(str(expense[4]))),
                                ft.DataCell(ft.Text(str(expense[5]))),
                                ft.DataCell(ft.Text(str(expense[6]))),
                            ]
                        )
                    )

                table_area.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("ID")),
                            ft.DataColumn(ft.Text("Category")),
                            ft.DataColumn(ft.Text("Description")),
                            ft.DataColumn(ft.Text("Amount")),
                            ft.DataColumn(ft.Text("Date")),
                            ft.DataColumn(ft.Text("Payment")),
                            ft.DataColumn(ft.Text("Status")),
                        ],
                        rows=rows
                    )
                )

            page.update()

        except Exception as e:
            show_message(f"Could not load expenses: {e}")

    def save_expense(e):
        cat = category.value
        desc = description.value.strip()
        date = expense_date.value.strip()
        pay = payment_method.value
        stat = status.value

        if not cat or not desc or not date:
            show_message("Fill all required fields.")
            return

        try:
            amount_value = float(amount.value)

            if amount_value <= 0:
                show_message("Amount must be positive.")
                return

            add_expense(cat, desc, amount_value, date, pay, stat)

            category.value = None
            description.value = ""
            amount.value = ""
            expense_date.value = ""
            payment_method.value = None
            status.value = None

            load_expenses()
            show_message("Expense saved successfully.")
            page.update()

        except Exception as e:
            show_message(f"Could not save expense: {e}")

    load_expenses()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Expenses", size=22, weight=ft.FontWeight.BOLD),
                ft.Row([category, description, amount], wrap=True),
                ft.Row([expense_date, payment_method, status], wrap=True),
                ft.Row([
                    ft.ElevatedButton("Save Expense", on_click=save_expense),
                    ft.OutlinedButton("Refresh Table", on_click=lambda e: load_expenses()),
                ]),
                ft.Divider(),
                ft.Text("Expenses List", size=18, weight=ft.FontWeight.BOLD),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )