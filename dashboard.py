from customtkinter import *
from database import cursor
from datetime import datetime, timedelta
import sqlite3



class DashboardManager:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
        
    def setup_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        title_label = CTkLabel(self.parent_frame, text="Pharmacy Dashboard", 
                             font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        self.tabview = CTkTabview(self.parent_frame)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.overview_tab = self.tabview.add("Overview")
        self.inventory_tab = self.tabview.add("Inventory")

        self.setup_overview_tab()
        self.setup_inventory_tab()

    def setup_overview_tab(self):
        stats_frame = CTkFrame(self.overview_tab)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cursor.execute("SELECT COUNT(*) FROM manufacturer")
        total_manufacturers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sales")
        total_sales = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total) FROM sales")
        total_revenue = cursor.fetchone()[0] or 0

        stats_data = [
            ("Total Manufacturers", total_manufacturers, "#4CAF50"),
            ("Total Medicines", total_medicines, "#2196F3"),
            ("Total Sales", total_sales, "#FF9800"),
            ("Total Revenue", f"${total_revenue:.2f}", "#E91E63")
        ]

        for i, (title, value, color) in enumerate(stats_data):
            row, col = divmod(i, 2)
            stat_card = CTkFrame(stats_frame)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            CTkLabel(stat_card, text=title, 
                    font=("Helvetica", 16)).pack(pady=5)
            CTkLabel(stat_card, text=str(value), 
                    font=("Helvetica", 24, "bold"), 
                    text_color=color).pack(pady=5)

        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)

    def setup_inventory_tab(self):
        inventory_frame = CTkScrollableFrame(self.inventory_tab)
        inventory_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cursor.execute("""
            SELECT m.med_name, c.cat_name, m.quantity, m.price
            FROM medicines m
            JOIN categories c ON m.cat_id = c.id
            WHERE m.quantity < 10
            ORDER BY m.quantity ASC
        """)
        low_stock = cursor.fetchall()

        header_label = CTkLabel(inventory_frame, text="Low Stock Alert", 
                                font=("Helvetica", 18, "bold"))
        header_label.grid(row=0, column=0, columnspan=4, pady=10)

        headers = ["Medicine", "Category", "Quantity", "Price"]
        for col, header in enumerate(headers):
            header_cell = CTkLabel(inventory_frame, text=header, font=("Helvetica", 12, "bold"))
            header_cell.grid(row=1, column=col, padx=10, pady=5, sticky="w")

        for row_index, item in enumerate(low_stock, start=2):
            med_name, cat_name, quantity, price = item

            CTkLabel(inventory_frame, text=med_name).grid(row=row_index, column=0, padx=10, pady=2, sticky="w")
            CTkLabel(inventory_frame, text=cat_name).grid(row=row_index, column=1, padx=10, pady=2, sticky="w")
            CTkLabel(inventory_frame, text=str(quantity),
                    text_color="#FF0000" if quantity < 5 else "white").grid(row=row_index, column=2, padx=10, pady=2, sticky="w")
            CTkLabel(inventory_frame, text=f"${price:.2f}").grid(row=row_index, column=3, padx=10, pady=2, sticky="w")

        # Optional: configure column weights for better resizing behavior
        for col in range(4):
            inventory_frame.grid_columnconfigure(col, weight=1)


def setup_dashboard_frame(parent_frame):
    DashboardManager(parent_frame)