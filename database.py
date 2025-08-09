import sqlite3

db = sqlite3.connect('pharmacy_management.db')
cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS manufacturer (id INTEGER PRIMARY KEY AUTOINCREMENT, mfr_name VARCHAR(25) NOT NULL, status VARCHAR(25) NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, cat_name VARCHAR(25) NOT NULL, status VARCHAR(25) NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS medicines (id INTEGER PRIMARY KEY AUTOINCREMENT, med_name VARCHAR(25) NOT NULL, mfr_id INTEGER NOT NULL, cat_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price INTEGER NOT NULL, FOREIGN KEY (mfr_id) REFERENCES manufacturer(id), FOREIGN KEY (cat_id) REFERENCES categories(id))')
cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    invoice_no INTEGER UNIQUE, 
    date DATE NOT NULL, 
    cust_name VARCHAR(25) NOT NULL, 
    contact_no INTEGER NOT NULL, 
    med_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL, 
    price INTEGER NOT NULL, 
    total INTEGER NOT NULL,
    FOREIGN KEY (med_id) REFERENCES medicines(id)
)''')
cursor.execute('CREATE TABLE IF NOT EXISTS purchase (id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_no INTEGER, date DATE NOT NULL, mfr_id INTEGER NOT NULL, cat_id INTEGER NOT NULL, med_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price INTEGER NOT NULL, total INTEGER NOT NULL, FOREIGN KEY (mfr_id) REFERENCES manufacturer(id), FOREIGN KEY (cat_id) REFERENCES categories(id), FOREIGN KEY (med_id) REFERENCES medicines(id))')
db.commit()