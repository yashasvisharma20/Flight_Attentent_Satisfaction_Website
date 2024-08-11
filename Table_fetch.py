import sqlite3

def check_db():
    conn = sqlite3.connect('customer_satisfaction.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(customer_satisfaction)")
    schema = cursor.fetchall()
    print("Table Schema:")
    for row in schema:
        print(row)

    cursor.execute("SELECT * FROM customer_satisfaction")
    rows = cursor.fetchall()
    print("\nTable Data:")
    for row in rows:
        print(row)

    conn.close()

if __name__ == '__main__':
    check_db()
