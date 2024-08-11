import sqlite3

def create_db():
    conn = sqlite3.connect('customer_satisfaction.db')
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS customer_satisfaction')
    
    c.execute('''
        CREATE TABLE customer_satisfaction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            flight_distance INTEGER,
            inflight_entertainment INTEGER,
            baggage_handling INTEGER,
            cleanliness INTEGER,
            departure_delay INTEGER,
            arrival_delay INTEGER,
            gender INTEGER,
            customer_type INTEGER,
            class TEXT,
            type_of_travel INTEGER,
            Class_Eco INTEGER DEFAULT 0,
            Class_Eco_Plus INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

create_db()
