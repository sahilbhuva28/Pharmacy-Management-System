from database import cursor, db
from utils import fetch_data, clear_input_fields
from CTkMessagebox import CTkMessagebox
from customtkinter import *

class MedicineManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
        
    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        title_label = CTkLabel(self.parent_frame, text="Medicine Management", 
                             font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

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
        form_title = CTkLabel(self.add_frame, text="Add Medicine", 
                            font=("Helvetica", 20, "bold"))
        form_title.pack(pady=(20, 30))

        form_container = CTkScrollableFrame(self.add_frame)
        form_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        cursor.execute("SELECT id, mfr_name FROM manufacturer WHERE status='Available'")
        self.manufacturers = {name: id for id, name in cursor.fetchall()}
        
        cursor.execute("SELECT id, cat_name FROM categories WHERE status='Available'")
        self.categories = {name: id for id, name in cursor.fetchall()}

        field_width = 220
        label_font = ("Helvetica", 12)
        pady_between = 8

        CTkLabel(form_container, text="Medicine Name:", font=label_font).pack(pady=(0, 2))
        self.name_entry = CTkEntry(form_container, width=field_width, height=32,
                                 placeholder_text="Enter medicine name")
        self.name_entry.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Manufacturer:", font=label_font).pack(pady=(0, 2))
        mfr_values = list(self.manufacturers.keys())
        self.mfr_menu = CTkOptionMenu(form_container, 
                                    values=mfr_values if mfr_values else ["No manufacturers"],
                                    width=field_width, height=32, corner_radius=0)
        self.mfr_menu.pack(pady=(0, pady_between))
        self.mfr_menu.set("Select Manufacturer")

        CTkLabel(form_container, text="Category:", font=label_font).pack(pady=(0, 2))
        cat_values = list(self.categories.keys())
        self.cat_menu = CTkOptionMenu(form_container, 
                                    values=cat_values if cat_values else ["No categories"],
                                    width=field_width, height=32, corner_radius=0)
        self.cat_menu.pack(pady=(0, pady_between))
        self.cat_menu.set("Select Category")

        CTkLabel(form_container, text="Quantity:", font=label_font).pack(pady=(0, 2))
        self.quantity_entry = CTkEntry(form_container, width=field_width, height=32,
                                     placeholder_text="Enter quantity")
        self.quantity_entry.pack(pady=(0, pady_between))

        CTkLabel(form_container, text="Price:", font=label_font).pack(pady=(0, 2))
        self.price_entry = CTkEntry(form_container, width=field_width, height=32,
                                  placeholder_text="Enter price")
        self.price_entry.pack(pady=(0, pady_between))

        CTkButton(self.add_frame, text="Add Medicine", 
                 command=self.add_medicine,
                 width=field_width, height=40,
                 font=("Helvetica", 14, "bold"), corner_radius=0).pack(pady=20)

    def setup_list_view(self, container):
        CTkLabel(container, text="Medicines List", 
                font=("Helvetica", 20, "bold")).pack(pady=(20, 15))

        search_frame = CTkFrame(container)
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        CTkLabel(search_frame, text="Search:", font=("Helvetica", 12)).pack(side="left", padx=5)
        self.search_entry = CTkEntry(search_frame, width=200, placeholder_text="Search by name...")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_list())

        self.list_frame = CTkScrollableFrame(container)
        self.list_frame.pack(fill="both", expand=True, padx=10)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        search_term = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""
        
        cursor.execute("""
            SELECT m.med_name, mfr.mfr_name, c.cat_name, m.quantity, m.price 
            FROM medicines m 
            JOIN manufacturer mfr ON m.mfr_id = mfr.id 
            JOIN categories c ON m.cat_id = c.id
            WHERE LOWER(m.med_name) LIKE ?
            ORDER BY m.med_name
        """, (f"%{search_term}%",))
        medicines = cursor.fetchall()

        headers = ["Name", "Manufacturer", "Category", "Quantity", "Price", "Actions"]
        header_font = ("Helvetica", 12, "bold")
        
        for col, header in enumerate(headers):
            self.list_frame.grid_columnconfigure(col, weight=1, minsize=100)
            CTkLabel(self.list_frame, text=header, 
                    font=header_font).grid(row=0, column=col, padx=10, pady=(5, 10), sticky="w")

        separator = CTkFrame(self.list_frame, height=2, fg_color="gray50")
        separator.grid(row=1, column=0, columnspan=len(headers), sticky="ew", pady=(0, 10))

        if not medicines:
            no_data_label = CTkLabel(self.list_frame, text="No medicines found", 
                                   font=("Helvetica", 12, "italic"))
            no_data_label.grid(row=2, column=0, columnspan=len(headers), pady=20)
            return

        for row, (name, mfr, cat, qty, price) in enumerate(medicines, start=2):
            CTkLabel(self.list_frame, text=name[:25] + "..." if len(name) > 25 else name)\
                .grid(row=row, column=0, padx=10, pady=2, sticky="w")
            CTkLabel(self.list_frame, text=mfr[:20] + "..." if len(mfr) > 20 else mfr)\
                .grid(row=row, column=1, padx=10, pady=2, sticky="w")
            CTkLabel(self.list_frame, text=cat[:20] + "..." if len(cat) > 20 else cat)\
                .grid(row=row, column=2, padx=10, pady=2, sticky="w")

            qty_color = "#FF0000" if qty < 10 else "#00FF00" if qty > 50 else "white"
            CTkLabel(self.list_frame, text=str(qty), text_color=qty_color)\
                .grid(row=row, column=3, padx=10, pady=2)

            CTkLabel(self.list_frame, text=f"${price:.2f}")\
                .grid(row=row, column=4, padx=10, pady=2)

            actions_frame = CTkFrame(self.list_frame)
            actions_frame.grid(row=row, column=5, padx=10, pady=2)

            current_data = (mfr, cat, qty, price)

            CTkButton(actions_frame, text="Edit", width=60, height=24,
                      command=lambda n=name, d=current_data: self.show_update_dialog(n, d),
                      corner_radius=0).pack(side="left", padx=2)
            CTkButton(actions_frame, text="Delete", width=60, height=24,
                      command=lambda n=name: self.show_delete_dialog(n),
                      corner_radius=0).pack(side="left", padx=2)

            if row < len(medicines) + 1:
                CTkFrame(self.list_frame, height=1, fg_color="gray30")\
                    .grid(row=row+1, column=0, columnspan=len(headers), sticky="ew")

    def add_medicine(self):
        name = self.name_entry.get()
        mfr_name = self.mfr_menu.get()
        cat_name = self.cat_menu.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if all([name, mfr_name, cat_name, quantity, price]) and \
           mfr_name not in ["No manufacturers", "Select Manufacturer"] and \
           cat_name not in ["No categories", "Select Category"]:
            try:
                cursor.execute("SELECT COUNT(*) FROM medicines WHERE LOWER(med_name) = LOWER(?)", (name,))
                if cursor.fetchone()[0] > 0:
                    CTkMessagebox(title="Error", message="Medicine already exists!", icon="warning")
                    return

                quantity = int(quantity)
                if quantity < 0:
                    CTkMessagebox(title="Error", message="Quantity cannot be negative!", icon="warning")
                    return

                price = float(price)
                if price <= 0:
                    CTkMessagebox(title="Error", message="Price must be greater than zero!", icon="warning")
                    return

                mfr_id = self.manufacturers[mfr_name]
                cat_id = self.categories[cat_name]

                cursor.execute("""
                    INSERT INTO medicines (med_name, mfr_id, cat_id, quantity, price)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, mfr_id, cat_id, quantity, price))

                db.commit()
                CTkMessagebox(title="Success", message="Medicine added successfully!", icon="check")

                self.name_entry.delete(0, 'end')
                self.quantity_entry.delete(0, 'end')
                self.price_entry.delete(0, 'end')
                self.mfr_menu.set("Select Manufacturer")
                self.cat_menu.set("Select Category")
                self.refresh_list()
            except ValueError:
                CTkMessagebox(title="Error", message="Invalid quantity or price!", icon="warning")
        else:
            CTkMessagebox(title="Error", message="Please fill all fields with valid values!", icon="warning")

    def show_update_dialog(self, old_name, current_data):
        main_window = self.parent_frame.winfo_toplevel()
        dialog = CTkToplevel(main_window)
        dialog.title("Update Medicine")
        dialog.geometry("400x600")

        dialog.update_idletasks()
        x = main_window.winfo_x() + (main_window.winfo_width() - dialog.winfo_width()) // 2
        y = main_window.winfo_y() + (main_window.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        dialog.transient(main_window)
        dialog.grab_set()

        CTkLabel(dialog, text="Update Medicine", font=("Helvetica", 20, "bold")).pack(pady=20)

        field_width = 250

        CTkLabel(dialog, text="New Name:").pack(pady=5)
        name_entry = CTkEntry(dialog, width=field_width)
        name_entry.insert(0, old_name)
        name_entry.pack(pady=5)

        CTkLabel(dialog, text="New Manufacturer:").pack(pady=5)
        mfr_menu = CTkOptionMenu(dialog, values=list(self.manufacturers.keys()),
                                 width=field_width, corner_radius=0)
        mfr_menu.set(current_data[0])
        mfr_menu.pack(pady=5)

        CTkLabel(dialog, text="New Category:").pack(pady=5)
        cat_menu = CTkOptionMenu(dialog, values=list(self.categories.keys()),
                                 width=field_width, corner_radius=0)
        cat_menu.set(current_data[1])
        cat_menu.pack(pady=5)

        CTkLabel(dialog, text="New Quantity:").pack(pady=5)
        quantity_entry = CTkEntry(dialog, width=field_width)
        quantity_entry.insert(0, str(current_data[2]))
        quantity_entry.pack(pady=5)

        CTkLabel(dialog, text="New Price:").pack(pady=5)
        price_entry = CTkEntry(dialog, width=field_width)
        price_entry.insert(0, str(current_data[3]))
        price_entry.pack(pady=5)

        def update():
            try:
                new_name = name_entry.get()
                new_mfr = mfr_menu.get()
                new_cat = cat_menu.get()
                new_quantity = int(quantity_entry.get())
                new_price = float(price_entry.get())

                if new_quantity < 0:
                    CTkMessagebox(title="Error", message="Quantity cannot be negative!", icon="warning")
                    return

                if new_price <= 0:
                    CTkMessagebox(title="Error", message="Price must be greater than zero!", icon="warning")
                    return

                cursor.execute("SELECT COUNT(*) FROM medicines WHERE LOWER(med_name) = LOWER(?) AND med_name != ?",
                               (new_name, old_name))
                if cursor.fetchone()[0] > 0:
                    CTkMessagebox(title="Error", message="Medicine name already exists!", icon="warning")
                    return

                mfr_id = self.manufacturers[new_mfr]
                cat_id = self.categories[new_cat]

                cursor.execute("""
                    UPDATE medicines 
                    SET med_name = ?, mfr_id = ?, cat_id = ?, quantity = ?, price = ? 
                    WHERE med_name = ?
                """, (new_name, mfr_id, cat_id, new_quantity, new_price, old_name))

                db.commit()
                CTkMessagebox(title="Success", message="Medicine updated successfully!", icon="check")
                dialog.destroy()
                self.refresh_list()
            except ValueError:
                CTkMessagebox(title="Error", message="Invalid quantity or price!", icon="warning")

        CTkButton(dialog, text="Update", command=update, width=field_width, corner_radius=0).pack(pady=20)

    def show_delete_dialog(self, name):
        main_window = self.parent_frame.winfo_toplevel()
        dialog = CTkToplevel(main_window)
        dialog.title("Confirm Deletion")
        dialog.geometry("300x150")

        dialog.update_idletasks()
        x = main_window.winfo_x() + (main_window.winfo_width() - dialog.winfo_width()) // 2
        y = main_window.winfo_y() + (main_window.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        dialog.transient(main_window)
        dialog.grab_set()

        CTkLabel(dialog, text=f"Are you sure you want to delete {name}?").pack(pady=20)

        def confirm_delete():
            cursor.execute("DELETE FROM medicines WHERE med_name = ?", (name,))
            db.commit()
            CTkMessagebox(title="Success", message="Medicine deleted successfully!", icon="check")
            dialog.destroy()
            self.refresh_list()

        buttons_frame = CTkFrame(dialog)
        buttons_frame.pack(pady=20)

        CTkButton(buttons_frame, text="Yes", command=confirm_delete, corner_radius=0).pack(side="left", padx=10)
        CTkButton(buttons_frame, text="No", command=dialog.destroy, corner_radius=0).pack(side="left", padx=10)

def setup_medicines_frame(parent_frame):
    MedicineManager(parent_frame)
