from flask import Flask, render_template, request
import sqlite3
import joblib

app = Flask(__name__)

model = joblib.load('logistic_Regression.lb')

def get_db_connection():
    conn = sqlite3.connect('customer_satisfaction.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/survey_form')
def survey_form():
    return render_template('survey.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form['inflight_entertainment'])
        baggage_handling = int(request.form['baggage_handling'])
        cleanliness = int(request.form['cleanliness'])
        departure_delay = int(request.form['departure_delay'])
        arrival_delay = int(request.form['arrival_delay'])
        gender = int(request.form['gender'])
        customer_type = int(request.form['customer_type'])
        travel_type = int(request.form['type_of_travel'])
        class_type = request.form['Class']

        Class_Eco = 0
        Class_Eco_Plus = 0
        if class_type == 'Eco':
            Class_Eco = 1
        elif class_type == 'Eco Plus':
            Class_Eco_Plus = 1

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO customer_satisfaction (
                age, flight_distance, inflight_entertainment, baggage_handling, cleanliness,
                departure_delay, arrival_delay, gender, customer_type, class, type_of_travel, Class_Eco, Class_Eco_Plus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (age, flight_distance, inflight_entertainment, baggage_handling, cleanliness,
              departure_delay, arrival_delay, gender, customer_type, class_type, travel_type, Class_Eco, Class_Eco_Plus))
        conn.commit()

        cursor = conn.execute('''
            SELECT age, flight_distance, inflight_entertainment, baggage_handling, cleanliness,
                   departure_delay, arrival_delay, gender, customer_type, type_of_travel, Class_Eco, Class_Eco_Plus
            FROM customer_satisfaction
            ORDER BY id DESC
            LIMIT 1
        ''')
        latest_data = cursor.fetchone()
        conn.close()

        latest_data_values = [
            latest_data['age'],
            latest_data['flight_distance'],
            latest_data['inflight_entertainment'],
            latest_data['baggage_handling'],
            latest_data['cleanliness'],
            latest_data['departure_delay'],
            latest_data['arrival_delay'],
            latest_data['gender'],
            latest_data['customer_type'],
            latest_data['type_of_travel'],
            latest_data['Class_Eco'],
            latest_data['Class_Eco_Plus']
        ]

        prediction = model.predict([latest_data_values])[0]
        labels = {'1': 'SATISFIED', '0': 'DISSATISFIED'}

        return render_template(
            'output.html',
            output=labels[str(prediction)],
            age=age,
            flight_distance=flight_distance,
            inflight_entertainment=inflight_entertainment,
            baggage_handling=baggage_handling,
            cleanliness=cleanliness,
            departure_delay=departure_delay,
            arrival_delay=arrival_delay,
            gender='Male' if gender == 1 else 'Female',
            customer_type='Loyal Customer' if customer_type == 0 else 'Disloyal Customer',
            class_type=class_type,
            travel_type='Personal Travel' if travel_type == 1 else 'Business Travel'
        )


if __name__ == '__main__':
    app.run(debug=True)
