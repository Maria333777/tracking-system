import flet as ft
from models import add_supplier, get_suppliers

def suppliers_view(page: ft.Page):
    company_name = ft.TextField(label="Company Name", width=250)
    phone = ft.TextField(label="Phone", width=200)
    email = ft.TextField(label="Email", width=250)

    table_area = ft.Column()

    def show_message(text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    def load_suppliers():
        table_area.controls.clear()

        try:
            suppliers = get_suppliers()

            if not suppliers:
                table_area.controls.append(ft.Text("No suppliers saved yet."))
            else:
                rows = []
                for supplier in suppliers:
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(supplier[0]))),
                                ft.DataCell(ft.Text(str(supplier[1]))),
                                ft.DataCell(ft.Text(str(supplier[2]))),
                                ft.DataCell(ft.Text(str(supplier[3]))),
                            ]
                        )
                    )

                table_area.controls.append(
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("ID")),
                            ft.DataColumn(ft.Text("Company")),
                            ft.DataColumn(ft.Text("Phone")),
                            ft.DataColumn(ft.Text("Email")),
                        ],
                        rows=rows
                    )
                )

            page.update()

        except Exception as e:
            show_message(f"Could not load suppliers: {e}")

    def save_supplier(e):
        name = company_name.value.strip()
        phone_value = phone.value.strip()
        email_value = email.value.strip()

        if name == "":
            show_message("Company name is required.")
            return

        try:
            add_supplier(name, phone_value, email_value)

            company_name.value = ""
            phone.value = ""
            email.value = ""

            load_suppliers()
            show_message("Supplier saved successfully.")

        except Exception as e:
            show_message(f"Could not save supplier: {e}")

    load_suppliers()

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Suppliers", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[company_name, phone, email],
                    wrap=True
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Save Supplier", on_click=save_supplier),
                    ]
                ),
                ft.Divider(),
                ft.Text("Suppliers List", size=18, weight=ft.FontWeight.BOLD),
                table_area,
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )