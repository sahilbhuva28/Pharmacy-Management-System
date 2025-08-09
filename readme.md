# 💊 Pharmacy Management System (Python + CustomTkinter)

A desktop application for managing a pharmacy’s daily operations, built with **Python**, **CustomTkinter**, and **SQLite3**.  
This application provides a secure login system using **bcrypt** for password hashing, a modern GUI with **CustomTkinter**, a date picker with **tkcalendar**, and user-friendly notifications via **CTkMessagebox**.

---

## ✨ Features

### 🔐 Secure Login System
- Passwords stored securely with **bcrypt** hashing.
- **Default Login:**

  Username: admin
  Password: admin123

````

* Ability to change password from within the app.

### 💊 Pharmacy Inventory Management

* Add, update, and delete medicines.
* Track quantities, expiry dates, and prices.

### 📦 Purchase Management

* Record purchases from suppliers.
* Update stock automatically when new medicines are purchased.
* Maintain supplier details for future reference.

### 📅 Expiry Date Management

* Highlight medicines nearing expiry using **tkcalendar**.

### 🎨 User-Friendly Interface

* Modern dark themes with **CustomTkinter**.
* Dialog boxes and alerts using **CTkMessagebox**.

---

## 📦 Requirements

### Python Version

* Python **3.8** or higher

### Install Dependencies

```bash
pip install bcrypt customtkinter tkcalendar CTkMessagebox
```

*(Standard library modules `sqlite3`, `tkinter`, and `datetime` come pre-installed with Python.)*

---

## 🚀 How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sahilbhuva28/pharmacy-management.git
cd pharmacy-management
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python login.py
```

---

## 🔑 Login with Default Credentials

```text
Username: admin
Password: admin123
```

---

## 🔄 Changing the Password

1. Log in with your current credentials.
2. Go to **Settings → Change Password**.
3. Enter your current password, then your new password twice.
4. The password will be securely updated in the database using **bcrypt** hashing.

---





