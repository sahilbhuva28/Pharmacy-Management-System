A desktop application for managing a pharmacy’s daily operations, built with **Python**, **CustomTkinter**, and **SQLite3**.  
This application provides a secure login system using **bcrypt** for password hashing, a modern GUI with **CustomTkinter**, a date picker with **tkcalendar**, and user-friendly notifications via **CTkMessagebox**.

---

## Features

- **Secure Login System**
  - Passwords stored securely with **bcrypt** hashing.
  - Default login:  
    - **Username:** `admin`  
    - **Password:** `admin123`  
  - Ability to change password from within the app.

- **Pharmacy Inventory Management**
  - Add, update, and delete medicines.
  - Track quantities, expiry dates, and prices.

- **Sales & Billing**
  - Record transactions.
  - Generate bills for customers.

- **Expiry Date Management**
  - Highlight medicines nearing expiry using **tkcalendar**.

- **User-Friendly Interface**
  - Modern dark/light themes with **CustomTkinter**.
  - Dialog boxes and alerts using **CTkMessagebox**.

---

## Requirements

### Python Version
- Python 3.8 or higher

### Install Dependencies
```bash
pip install bcrypt customtkinter tkcalendar CTkMessagebox

(Standard library modules sqlite3, tkinter, and datetime come pre-installed with Python.)

How to Run


Clone the Repository
bashCopyEditgit clone https://github.com/sahilbhuva28/pharmacy-management.git
cd pharmacy-management



Install Requirements
bashCopyEditpip install -r requirements.txt



Run the Application
bashCopyEditpython main.py



Login with Default Credentials


Username: admin


Password: admin123





Changing the Password


Log in with your current credentials.


Go to Settings > Change Password.


Enter your current password, then your new password twice.


The password will be securely updated in the database using bcrypt hashing.