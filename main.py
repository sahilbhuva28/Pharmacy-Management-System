from customtkinter import *
from tkcalendar import Calendar
from database import db
from manufacturer import setup_manufacturer_frame
from categories import setup_categories_frame
from medicines import setup_medicines_frame
from sales import setup_sales_frame
from purchase import setup_purchase_frame
from dashboard import setup_dashboard_frame
from change_password import change_password  # ⬅️ Add this import

def start_main_application(username):  # ⬅️ Accept username
    root = CTk()
    root.title("Pharmacy Management System")

    width = 1330
    height = 700
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    main_container = CTkFrame(root)
    main_container.pack(fill="both", expand=True)

    sidebar = CTkFrame(main_container, fg_color="#333333", corner_radius=0, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content_frame = CTkFrame(main_container, fg_color="#f0f0f0")
    content_frame.pack(side="left", fill="both", expand=True)

    frames = {
        "dashboard": CTkFrame(content_frame),
        "manufacturer": CTkFrame(content_frame),
        "categories": CTkFrame(content_frame),
        "medicines": CTkFrame(content_frame),
        "sales": CTkFrame(content_frame),
        "purchase": CTkFrame(content_frame)
    }

    for frame in frames.values():
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(frame_name):
        for frame in frames.values():
            frame.place_forget()

        frame = frames[frame_name]
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        if frame_name == "dashboard":
            setup_dashboard_frame(frame)
        elif frame_name == "manufacturer":
            setup_manufacturer_frame(frame)
        elif frame_name == "categories":
            setup_categories_frame(frame)
        elif frame_name == "medicines":
            setup_medicines_frame(frame)
        elif frame_name == "sales":
            setup_sales_frame(frame)
        elif frame_name == "purchase":
            setup_purchase_frame(frame)

    buttons_data = [
        ("Dashboard", "dashboard"),
        ("Manufacturer", "manufacturer"),
        ("Categories", "categories"),
        ("Medicines", "medicines"),
        ("Sales", "sales"),
        ("Purchase", "purchase")
    ]

    for text, frame_name in buttons_data:
        btn = CTkButton(
            sidebar,
            text=text,
            corner_radius=0,
            height=40,
            width=200,
            fg_color="#333333",
            hover_color="#555555",
            border_width=2,
            command=lambda f=frame_name: show_frame(f)
        )
        btn.pack(pady=5)

    # 🔒 Change Password Button
    CTkButton(
        sidebar,
        text="Change Password",
        corner_radius=0,
        height=40,
        width=200,
        fg_color="#333333",
        hover_color="#444444",
        border_width=2,
        command=lambda: change_password(username)
    ).pack(pady=(30, 5))

    show_frame("dashboard")

    root.mainloop()

if __name__ == "__main__":
    print("Please run login.py to start the application!")
