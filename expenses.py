import flet as ft
from models import add_expense, get_expenses, update_expense, delete_expense

def expenses_view(page: ft.Page):
    category = ft.Dropdown(
        label="Category",
        width=180,
        options=[
            ft.dropdown.Option("Office Supplies"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("Maintenance"),
            ft.dropdown.Option("Utilities"),
            ft.dropdown.Option("Other"),
        ]
    )

    description = ft.TextField(label="Description", width=240)
    amount = ft.TextField(label="Amount", width=120)
    expense_date = ft.TextField(label="Expense Date", hint_text="YYYY-MM-DD", width=180)

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

    editing_id = None
    editing_text = ft.Text("Editing: none")
    table_area = ft.Column()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def clear_form(e=None):
        nonlocal editing_id
        editing_id = None
        category.value = None
        description.value = ""
        amount.value = ""
        expense_date.value = ""
        payment_method.value = None
        status.value = None
        editing_text.value = "Editing: none"
        page.update()

    def fill_form(expense):
        nonlocal editing_id
        editing_id = expense[0]
        category.value = expense[1]
        description.value = expense[2]
        amount.value = str(expense[3])
        expense_date.value = expense[4]
        payment_method.value = expense[5]
        status.value = expense[6]
        editing_text.value = f"Editing expense ID: {editing_id}"
        page.update()

    def save_expense_data(e):
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

            clear_form()
            load_expenses()
            show_message("Expense saved.")
        except Exception as error:
            show_message(f"Error: {error}")

    def update_expense_data(e):
        if editing_id is None:
            show_message("Pick an expense first.")
            return

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

            update_expense(editing_id, cat, desc, amount_value, date, pay, stat)

            clear_form()
            load_expenses()
            show_message("Expense updated.")
        except Exception as error:
            show_message(f"Error: {error}")

    def remove_expense(expense_id):
        try:
            delete_expense(expense_id)
            clear_form()
            load_expenses()
            show_message("Expense deleted.")
        except Exception as error:
            show_message(f"Error: {error}")

    def load_expenses():
        table_area.controls.clear()
        expenses = get_expenses()

        if not expenses:
            table_area.controls.append(ft.Text("No expenses yet."))
        else:
            rows = []

            for expense in expenses:
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
                            ft.DataCell(
                                ft.TextButton(
                                    "Edit",
                                    on_click=lambda e, expense=expense: fill_form(expense)
                                )
                            ),
                            ft.DataCell(
                                ft.TextButton(
                                    "Delete",
                                    on_click=lambda e, expense_id=expense[0]: remove_expense(expense_id)
                                )
                            ),
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
                        ft.DataColumn(ft.Text("Edit")),
                        ft.DataColumn(ft.Text("Delete")),
                    ],
                    rows=rows
                )
            )

        page.update()

    load_expenses()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Expenses", size=22, weight=ft.FontWeight.BOLD),
                editing_text,
                ft.Row([category, description, amount], wrap=True),
                ft.Row([expense_date, payment_method, status], wrap=True),
                ft.Row(
                    [
                        ft.ElevatedButton("Save", on_click=save_expense_data),
                        ft.ElevatedButton("Update", on_click=update_expense_data),
                        ft.OutlinedButton("Clear", on_click=clear_form),
                        ft.OutlinedButton("Refresh", on_click=lambda e: load_expenses()),
                    ],
                    wrap=True
                ),
                ft.Divider(),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )