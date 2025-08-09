from database import cursor, db
from utils import fetch_data, clear_input_fields
from CTkMessagebox import CTkMessagebox
from customtkinter import *

class CategoryManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.parent_frame, text="Category Management",
                 font=("Helvetica", 24, "bold")).pack(pady=20)

        main_container = CTkFrame(self.parent_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.add_frame = CTkFrame(main_container)
        self.add_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10, ipadx=20)

        list_container = CTkFrame(main_container)
        list_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_add_form()
        self.setup_list_view(list_container)

    def setup_add_form(self):
        CTkLabel(self.add_frame, text="Add Category",
                 font=("Helvetica", 18, "bold")).pack(pady=15)

        CTkLabel(self.add_frame, text="Category Name:").pack(pady=5)
        self.name_entry = CTkEntry(self.add_frame, width=200, corner_radius=0)
        self.name_entry.pack(pady=5)

        CTkLabel(self.add_frame, text="Status:").pack(pady=5)
        self.status_menu = CTkOptionMenu(self.add_frame,
                                         values=["Not Selected", "Available", "Not Available"],
                                         width=200, corner_radius=0)
        self.status_menu.set("Not Selected")
        self.status_menu.pack(pady=5)

        CTkButton(self.add_frame, text="Add Category",
                  command=self.add_category, width=200, corner_radius=0).pack(pady=20)

    def setup_list_view(self, container):
        CTkLabel(container, text="Categories List",
                 font=("Helvetica", 18, "bold")).pack(pady=15)

        self.list_frame = CTkScrollableFrame(container)
        self.list_frame.pack(fill="both", expand=True)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        cursor.execute("SELECT cat_name, status FROM categories")
        categories = cursor.fetchall()

        headers = ["Name", "Status", "Actions"]
        for col, header in enumerate(headers):
            CTkLabel(self.list_frame, text=header,
                     font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        for row, (name, status) in enumerate(categories, start=1):
            CTkLabel(self.list_frame, text=name).grid(row=row, column=0, padx=10, pady=2)
            CTkLabel(self.list_frame, text=status).grid(row=row, column=1, padx=10, pady=2)

            actions_frame = CTkFrame(self.list_frame)
            actions_frame.grid(row=row, column=2, padx=10, pady=2)

            CTkButton(actions_frame, text="Edit",
                      command=lambda n=name, s=status: self.show_update_dialog(n, s),
                      corner_radius=0).pack(side="left", padx=2)
            CTkButton(actions_frame, text="Delete",
                      command=lambda n=name: self.show_delete_dialog(n),
                      corner_radius=0).pack(side="left", padx=2)

    def add_category(self):
        name = self.name_entry.get().strip()
        status = self.status_menu.get()

        if name and status != "Not Selected":
            cursor.execute("SELECT COUNT(*) FROM categories WHERE LOWER(cat_name) = LOWER(?)", (name,))
            if cursor.fetchone()[0] > 0:
                CTkMessagebox(title="Error", message="Category already exists!", icon="warning")
                return

            cursor.execute("INSERT INTO categories (cat_name, status) VALUES (?, ?)", (name, status))
            db.commit()
            CTkMessagebox(title="Success", message="Category added successfully!", icon="check")

            self.name_entry.delete(0, 'end')
            self.status_menu.set("Not Selected")
            self.refresh_list()
        else:
            CTkMessagebox(title="Error", message="Please enter a name and select a valid status.", icon="warning")

    def show_update_dialog(self, old_name, current_status):
        main_window = self.parent_frame.winfo_toplevel()
        dialog = CTkToplevel(main_window)
        dialog.title("Update Category")
        dialog.geometry("400x300")

        dialog.update_idletasks()
        x = main_window.winfo_x() + (main_window.winfo_width() - dialog.winfo_width()) // 2
        y = main_window.winfo_y() + (main_window.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        dialog.transient(main_window)
        dialog.grab_set()

        CTkLabel(dialog, text="Update Category",
                 font=("Helvetica", 20, "bold")).pack(pady=20)

        CTkLabel(dialog, text="New Name:").pack(pady=5)
        name_entry = CTkEntry(dialog, corner_radius=0)
        name_entry.insert(0, old_name)
        name_entry.pack(pady=5)

        CTkLabel(dialog, text="New Status:").pack(pady=5)
        status_menu = CTkOptionMenu(dialog,
                                    values=["Not Selected", "Available", "Not Available"],
                                    corner_radius=0)
        status_menu.set(current_status)
        status_menu.pack(pady=5)

        def update():
            new_name = name_entry.get().strip()
            new_status = status_menu.get()

            if new_name and new_status != "Not Selected":
                cursor.execute("SELECT COUNT(*) FROM categories WHERE LOWER(cat_name) = LOWER(?) AND cat_name != ?",
                               (new_name, old_name))
                if cursor.fetchone()[0] > 0:
                    CTkMessagebox(title="Error", message="Category name already exists!", icon="warning")
                    return

                cursor.execute("UPDATE categories SET cat_name = ?, status = ? WHERE cat_name = ?",
                               (new_name, new_status, old_name))
                db.commit()
                CTkMessagebox(title="Success", message="Category updated successfully!", icon="check")
                dialog.destroy()
                self.refresh_list()
            else:
                CTkMessagebox(title="Error", message="Please enter a name and select a valid status.", icon="warning")

        CTkButton(dialog, text="Update", command=update, corner_radius=0).pack(pady=20)

    def show_delete_dialog(self, name):
        confirm = CTkMessagebox(
            title="Confirm Delete",
            message=f"Are you sure you want to delete '{name}'?",
            icon="warning", option_1="Yes", option_2="No",corner_radius=0
        )
        if confirm.get() == "Yes":
            cursor.execute("DELETE FROM categories WHERE cat_name = ?", (name,))
            db.commit()
            CTkMessagebox(title="Deleted", message="Category deleted successfully!", icon="check")
            self.refresh_list()

def setup_categories_frame(parent_frame):
    CategoryManager(parent_frame)
