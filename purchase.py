from database import cursor, db
from utils import fetch_data, clear_input_fields, validate_date
from CTkMessagebox import CTkMessagebox
from customtkinter import *
from tkcalendar import DateEntry
from datetime import datetime

class PurchaseManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.parent_frame, text="Purchase Management", font=("Helvetica", 24, "bold")).pack(pady=20)

        main_container = CTkFrame(self.parent_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.add_frame = CTkFrame(main_container, width=300)
        self.add_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)
        self.add_frame.pack_propagate(False)

        list_container = CTkFrame(main_container)
        list_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_add_form()
        self.setup_list_view(list_container)

    def setup_add_form(self):
        CTkLabel(self.add_frame, text="Add Purchase", font=("Helvetica", 20, "bold")).pack(pady=(20, 30))

        form_container = CTkScrollableFrame(self.add_frame)
        form_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        cursor.execute("SELECT id, mfr_name FROM manufacturer WHERE status='Available'")
        self.manufacturers = {name: id for id, name in cursor.fetchall()}

        cursor.execute("SELECT id, cat_name FROM categories WHERE status='Available'")
        self.categories = {name: id for id, name in cursor.fetchall()}

        cursor.execute("SELECT id, med_name FROM medicines")
        self.medicines = {name: id for id, name in cursor.fetchall()}

        field_width = 220
        label_font = ("Helvetica", 12)
        pady_between = 8

        CTkLabel(form_container, text="Invoice Number:", font=label_font).pack(pady=(0, 2))
        self.invoice_entry = CTkEntry(form_container, width=field_width, height=32, corner_radius=0, placeholder_text="Enter invoice number")
        self.invoice_entry.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Date:", font=label_font).pack(pady=(0, 2))
        date_frame = CTkFrame(form_container)
        date_frame.pack(pady=(0, pady_between))
        self.date_picker = DateEntry(date_frame, width=16, background='darkblue', foreground='white', borderwidth=2, font=('Helvetica', 10))
        self.date_picker.pack(pady=5)

        CTkLabel(form_container, text="Manufacturer:", font=label_font).pack(pady=(0, 2))
        mfr_values = ["Not Selected"] + list(self.manufacturers.keys())
        self.mfr_menu = CTkOptionMenu(form_container, values=mfr_values, width=field_width, height=32, corner_radius=0)
        self.mfr_menu.set("Not Selected")
        self.mfr_menu.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Category:", font=label_font).pack(pady=(0, 2))
        cat_values = ["Not Selected"] + list(self.categories.keys())
        self.cat_menu = CTkOptionMenu(form_container, values=cat_values, width=field_width, height=32, corner_radius=0)
        self.cat_menu.set("Not Selected")
        self.cat_menu.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Medicine:", font=label_font).pack(pady=(0, 2))
        med_values = ["Not Selected"] + list(self.medicines.keys())
        self.med_menu = CTkOptionMenu(form_container, values=med_values, width=field_width, height=32, corner_radius=0)
        self.med_menu.set("Not Selected")
        self.med_menu.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Quantity:", font=label_font).pack(pady=(0, 2))
        self.quantity_entry = CTkEntry(form_container, width=field_width, height=32, corner_radius=0, placeholder_text="Enter quantity")
        self.quantity_entry.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Price per unit:", font=label_font).pack(pady=(0, 2))
        self.price_entry = CTkEntry(form_container, width=field_width, height=32, corner_radius=0, placeholder_text="Enter price per unit")
        self.price_entry.pack(pady=(0, pady_between))

        CTkButton(self.add_frame, text="Add Purchase", command=self.add_purchase, width=field_width, height=40, font=("Helvetica", 14, "bold"), corner_radius=0).pack(pady=20)

    def setup_list_view(self, container):
        CTkLabel(container, text="Purchase History", font=("Helvetica", 20, "bold")).pack(pady=(20, 15))
        self.list_frame = CTkScrollableFrame(container)
        self.list_frame.pack(fill="both", expand=True, padx=10)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        cursor.execute("""
            SELECT p.id, p.invoice_no, p.date, mfr.mfr_name, c.cat_name, 
                   m.med_name, p.quantity, p.price, p.total
            FROM purchase p
            JOIN manufacturer mfr ON p.mfr_id = mfr.id
            JOIN categories c ON p.cat_id = c.id
            JOIN medicines m ON p.med_id = m.id
            ORDER BY p.date DESC
        """)
        purchases = cursor.fetchall()

        headers = ["Invoice", "Date", "Manufacturer", "Category", "Medicine", "Qty", "Price", "Total", "Action"]
        for col, header in enumerate(headers):
            self.list_frame.grid_columnconfigure(col, weight=1, minsize=90)
            CTkLabel(self.list_frame, text=header, font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=5, pady=(5, 10), sticky="w")

        for row_idx, purchase in enumerate(purchases, start=1):
            purchase_id = purchase[0]
            for col_idx, value in enumerate(purchase[1:]):
                text = f"${value:.2f}" if isinstance(value, float) and col_idx in [6, 7] else str(value)
                sticky = "e" if isinstance(value, (int, float)) else "w"
                CTkLabel(self.list_frame, text=text, font=("Helvetica", 11)).grid(row=row_idx, column=col_idx, padx=5, pady=4, sticky=sticky)

            delete_btn = CTkButton(self.list_frame, text="Delete", command=lambda pid=purchase_id: self.delete_purchase(pid), corner_radius=0)
            delete_btn.grid(row=row_idx, column=len(headers) - 1, padx=5, pady=4)

    def delete_purchase(self, purchase_id):
        confirm = CTkMessagebox(title="Confirm Delete", message="Are you sure you want to delete this purchase?", icon="warning", option_1="Yes", option_2="No")
        if confirm.get() == "Yes":
            cursor.execute("SELECT quantity, med_id FROM purchase WHERE id = ?", (purchase_id,))
            result = cursor.fetchone()
            if result:
                qty, med_id = result
                cursor.execute("DELETE FROM purchase WHERE id = ?", (purchase_id,))
                cursor.execute("UPDATE medicines SET quantity = quantity - ? WHERE id = ?", (qty, med_id))
                db.commit()
                self.refresh_list()
                CTkMessagebox(title="Deleted", message="Purchase deleted successfully!", icon="check")

    def calculate_total(self):
        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            return quantity * price
        except ValueError:
            return 0

    def add_purchase(self):
        invoice_no = self.invoice_entry.get().strip()
        date = self.date_picker.get_date()
        mfr_name = self.mfr_menu.get()
        cat_name = self.cat_menu.get()
        med_name = self.med_menu.get()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if any(x == "Not Selected" for x in [mfr_name, cat_name, med_name]):
            CTkMessagebox(title="Error", message="Please select valid Manufacturer, Category, and Medicine.", icon="warning")
            return

        cursor.execute("SELECT COUNT(*) FROM purchase WHERE invoice_no = ?", (invoice_no,))
        if cursor.fetchone()[0] > 0:
            CTkMessagebox(title="Error", message="Invoice number already exists!", icon="warning")
            return

        if not validate_date(date.strftime('%Y-%m-%d')):
            CTkMessagebox(title="Error", message="Please select today's date or a future date!", icon="warning")
            return

        if all([invoice_no, date, quantity, price]):
            try:
                quantity = int(quantity)
                price = float(price)
                total = self.calculate_total()

                mfr_id = self.manufacturers[mfr_name]
                cat_id = self.categories[cat_name]
                med_id = self.medicines[med_name]

                cursor.execute('''
                    INSERT INTO purchase (invoice_no, date, mfr_id, cat_id, med_id, quantity, price, total)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (invoice_no, date.strftime('%Y-%m-%d'), mfr_id, cat_id, med_id, quantity, price, total))

                cursor.execute("UPDATE medicines SET quantity = quantity + ? WHERE id = ?", (quantity, med_id))
                db.commit()

                CTkMessagebox(title="Success", message="Purchase recorded successfully!", icon="check")

                self.invoice_entry.delete(0, 'end')
                self.quantity_entry.delete(0, 'end')
                self.price_entry.delete(0, 'end')
                self.mfr_menu.set("Not Selected")
                self.cat_menu.set("Not Selected")
                self.med_menu.set("Not Selected")

                self.refresh_list()
            except ValueError:
                CTkMessagebox(title="Error", message="Invalid quantity or price!", icon="warning")
        else:
            CTkMessagebox(title="Error", message="Please fill all fields!", icon="warning")

def setup_purchase_frame(parent_frame):
    PurchaseManager(parent_frame)
