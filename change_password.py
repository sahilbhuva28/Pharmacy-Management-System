from customtkinter import *
from CTkMessagebox import CTkMessagebox
import sqlite3
import bcrypt

db = sqlite3.connect('pharmacy_management.db')
cursor = db.cursor()

def change_password(current_username):
    pw_window = CTk()
    pw_window.title("Change Password")

    width = 400
    height = 400
    x = (pw_window.winfo_screenwidth() - width) // 2
    y = (pw_window.winfo_screenheight() - height) // 2
    pw_window.geometry(f"{width}x{height}+{x}+{y}")
    pw_window.resizable(False, False)

    def update_password():
        current_pw = current_password_entry.get()
        new_pw = new_password_entry.get()
        confirm_pw = confirm_password_entry.get()

        cursor.execute("SELECT password FROM login WHERE username=?", (current_username,))
        result = cursor.fetchone()

        if not result or not bcrypt.checkpw(current_pw.encode(), result[0]):
            CTkMessagebox(title="Error", message="Current password is incorrect", icon="cancel")
            return

        if new_pw != confirm_pw:
            CTkMessagebox(title="Error", message="New passwords do not match", icon="cancel")
            return

        if len(new_pw) < 6:
            CTkMessagebox(title="Error", message="Password must be at least 6 characters long", icon="warning")
            return

        hashed_new_pw = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())
        cursor.execute("UPDATE login SET password=? WHERE username=?", (hashed_new_pw, current_username))
        db.commit()
        CTkMessagebox(title="Success", message="Password updated successfully!", icon="check")
        pw_window.destroy()

    CTkLabel(pw_window, text="Current Password", font=("Helvetica", 15)).pack(pady=(40, 5))
    current_password_entry = CTkEntry(pw_window, show="*", font=("Helvetica", 12), width=250,corner_radius=0)
    current_password_entry.pack()

    CTkLabel(pw_window, text="New Password", font=("Helvetica", 15)).pack(pady=(20, 5))
    new_password_entry = CTkEntry(pw_window, show="*", font=("Helvetica", 12), width=250,corner_radius=0)
    new_password_entry.pack()

    CTkLabel(pw_window, text="Confirm New Password", font=("Helvetica", 15)).pack(pady=(20, 5))
    confirm_password_entry = CTkEntry(pw_window, show="*", font=("Helvetica", 12), width=250,corner_radius=0)
    confirm_password_entry.pack()

    CTkButton(pw_window, text="Update Password", font=("Helvetica", 15), width=200,
              corner_radius=0, hover_color="green", command=update_password).pack(pady=30)

    pw_window.mainloop()
