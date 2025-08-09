from database import cursor, db
from utils import validate_date
from CTkMessagebox import CTkMessagebox
from customtkinter import *
from tkcalendar import DateEntry
from datetime import datetime

class SalesManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.parent_frame, text="Sales Management", font=("Helvetica", 24, "bold")).pack(pady=20)

        main_container = CTkFrame(self.parent_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.add_frame = CTkFrame(main_container)
        self.add_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10, ipadx=20)

        list_container = CTkFrame(main_container)
        list_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_add_form()
        self.setup_list_view(list_container)

    def setup_add_form(self):
        CTkLabel(self.add_frame, text="Add Sale", font=("Helvetica", 18, "bold")).pack(pady=15)

        cursor.execute("""
            SELECT m.id, m.med_name, c.cat_name, m.price 
            FROM medicines m 
            JOIN categories c ON m.cat_id = c.id
            WHERE m.quantity > 0
        """)
        self.medicines = {
            f"{med_name} ({cat_name})": (mid, price)
            for mid, med_name, cat_name, price in cursor.fetchall()
        }

        entries = [
            ("Invoice Number:", "placeholder", "Enter invoice number", "invoice_entry"),
            ("Customer Name:", "placeholder", "Enter customer name", "customer_entry"),
            ("Contact Number:", "placeholder", "Enter contact number", "contact_entry"),
            ("Quantity:", "placeholder", "Enter quantity", "quantity_entry"),
        ]
        for label_text, _, placeholder, attr in entries:
            CTkLabel(self.add_frame, text=label_text).pack(pady=5)
            setattr(self, attr, CTkEntry(self.add_frame, width=200, corner_radius=0, placeholder_text=placeholder))
            getattr(self, attr).pack(pady=5)

        CTkLabel(self.add_frame, text="Date:").pack(pady=5)
        date_frame = CTkFrame(self.add_frame)
        date_frame.pack(pady=5)
        self.date_picker = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_picker.pack()

        CTkLabel(self.add_frame, text="Medicine:").pack(pady=5)
        medicine_values = ["Not Selected"] + list(self.medicines.keys()) if self.medicines else ["No medicines available"]
        self.medicine_menu = CTkOptionMenu(
            self.add_frame,
            values=medicine_values,
            width=200,
            corner_radius=0
        )
        self.medicine_menu.set("Not Selected")
        self.medicine_menu.pack(pady=5)

        CTkButton(self.add_frame, text="Add Sale", command=self.add_sale, width=200, corner_radius=0).pack(pady=20)

    def setup_list_view(self, container):
        CTkLabel(container, text="Sales List", font=("Helvetica", 18, "bold")).pack(pady=15)
        self.list_frame = CTkScrollableFrame(container)
        self.list_frame.pack(fill="both", expand=True)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        cursor.execute("""
            SELECT s.id, s.invoice_no, s.date, s.cust_name, s.contact_no,
                   m.med_name, s.quantity, s.price, s.total
            FROM sales s
            JOIN medicines m ON s.med_id = m.id
            ORDER BY s.date DESC
        """)
        sales = cursor.fetchall()

        headers = ["Invoice", "Date", "Customer", "Contact", "Medicine", "Qty", "Price", "Total", "Action"]
        for col, h in enumerate(headers):
            CTkLabel(self.list_frame, text=h, font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        for r, row in enumerate(sales, start=1):
            sale_id, *vals = row
            for c, val in enumerate(vals):
                txt = f"${val:.2f}" if isinstance(val, float) and c in [6, 7] else str(val)
                CTkLabel(self.list_frame, text=txt).grid(row=r, column=c, padx=10, pady=2)

            CTkButton(self.list_frame, text="Delete",
                      command=lambda sid=sale_id: self.delete_sale(sid),
                      corner_radius=0).grid(row=r, column=len(headers)-1, padx=10, pady=2)

    def delete_sale(self, sale_id):
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message="Delete this sale and restore inventory?",
            icon="warning", option_1="Yes", option_2="No"
        )
        if confirm.get() == "Yes":
            cursor.execute("SELECT quantity, med_id FROM sales WHERE id = ?", (sale_id,))
            row = cursor.fetchone()
            if row:
                qty, mid = row
                cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
                cursor.execute("UPDATE medicines SET quantity = quantity + ? WHERE id = ?", (qty, mid))
                db.commit()
                CTkMessagebox(title="Deleted", message="Sale removed and stock updated.", icon="check")
                self.refresh_list()

    def calculate_total(self):
        try:
            sel = self.medicine_menu.get()
            if sel not in self.medicines:
                return 0
            qty = int(self.quantity_entry.get())
            _, price = self.medicines[sel]
            return qty * price
        except:
            return 0

    def add_sale(self):
        if not self.medicines:
            CTkMessagebox(title="Error", message="No medicines available!", icon="warning")
            return

        data = {
            'invoice': self.invoice_entry.get().strip(),
            'date': self.date_picker.get_date(),
            'cust': self.customer_entry.get().strip(),
            'contact': self.contact_entry.get().strip(),
            'med_sel': self.medicine_menu.get(),
            'qty': self.quantity_entry.get().strip()
        }

        if data['med_sel'] in ["Not Selected", "No medicines available"]:
            return CTkMessagebox(title="Error", message="Please select a valid medicine!", icon="warning")

        cursor.execute("SELECT COUNT(*) FROM sales WHERE invoice_no = ?", (data['invoice'],))
        if cursor.fetchone()[0] > 0:
            return CTkMessagebox(title="Error", message="Invoice already exists!", icon="warning")

        if not validate_date(data['date'].strftime('%Y-%m-%d')):
            return CTkMessagebox(title="Error", message="Select current or future date!", icon="warning")

        if all(data.values()):
            try:
                qty = int(data['qty'])
                mid, price = self.medicines[data['med_sel']]
                cursor.execute("SELECT quantity FROM medicines WHERE id = ?", (mid,))
                stock = cursor.fetchone()[0]
                if qty > stock:
                    return CTkMessagebox(
                        title="Error",
                        message=f"Only {stock} units in stock.",
                        icon="warning"
                    )
                total = self.calculate_total()
                cursor.execute("UPDATE medicines SET quantity = quantity - ? WHERE id = ?", (qty, mid))
                cursor.execute("""
                    INSERT INTO sales (invoice_no, date, cust_name, contact_no, med_id, quantity, price, total)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (data['invoice'], data['date'].strftime('%Y-%m-%d'),
                      data['cust'], data['contact'], mid, qty, price, total))
                db.commit()
                CTkMessagebox(title="Success", message="Sale added!", icon="check")
                for field in ("invoice_entry", "customer_entry", "contact_entry", "quantity_entry"):
                    getattr(self, field).delete(0, 'end')
                self.medicine_menu.set("Not Selected")
                self.refresh_list()
            except ValueError:
                CTkMessagebox(title="Error", message="Invalid quantity!", icon="warning")
        else:
            CTkMessagebox(title="Error", message="Please fill all fields!", icon="warning")

def setup_sales_frame(parent_frame):
    SalesManager(parent_frame)
