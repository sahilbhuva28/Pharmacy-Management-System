from database import cursor
from datetime import datetime

def fetch_data(query, params=()):
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return rows

def clear_input_fields(entries):
    for entry in entries:
        entry.delete(0, 'end')

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return date >= today
    except ValueError:
        return False