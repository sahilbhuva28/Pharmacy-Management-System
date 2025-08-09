from tkinter import *
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import sqlite3
import bcrypt
from main import start_main_application

db = sqlite3.connect('pharmacy_management.db')
cursor = db.cursor()

# Create login table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password BLOB NOT NULL
)
''')

# Insert default admin if not exists
cursor.execute('SELECT * FROM login WHERE username = "admin"')
if not cursor.fetchone():
    hashed_password = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
    cursor.execute('INSERT INTO login (username, password) VALUES (?, ?)', ('admin', hashed_password))
    db.commit()

def checklogin():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute('SELECT password FROM login WHERE username=?', (username,))
    row = cursor.fetchone()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        root.after(500, lambda: close_and_start_main(username))
    else:
        CTkMessagebox(title="Error", message="Invalid Username and Password", icon="warning")

def close_and_start_main(username):
    root.destroy()
    start_main_application(username)

def start_login():
    set_appearance_mode("dark")

    global root
    root = CTk()
    root.title("Pharmacy Management System - Login")

    width = 400
    height = 350
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    username_label = CTkLabel(root, text="Username:", font=("Helvetica", 15, "bold"), anchor="nw")
    username_label.pack(fill="x", pady=(50, 5), padx=80)

    global username_entry
    username_entry = CTkEntry(root, font=("Helvetica", 12), width=250, corner_radius=0)
    username_entry.pack(pady=5)

    password_label = CTkLabel(root, text="Password:", font=("Helvetica", 15, "bold"), anchor="nw")
    password_label.pack(fill="x", pady=(20, 5), padx=80)

    global password_entry
    password_entry = CTkEntry(root, show="*", font=("Helvetica", 12), width=250, corner_radius=0)
    password_entry.pack(pady=(5, 20))

    sign_in_button = CTkButton(root, text="Sign In", font=("Helvetica", 15), width=200,
                               corner_radius=0, hover_color="green", command=checklogin)
    sign_in_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_login()
