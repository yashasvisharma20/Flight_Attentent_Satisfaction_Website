from flask import Flask, render_template, request
import joblib

model = joblib.load('logistic_Regression.lb')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project_form')
def project():
    return render_template('project.html')

@app.route("/submit_form", methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        try:
            age = int(request.form['age'])
            flight_distance = int(request.form['flight_distance'])
            inflight_entertainment = int(request.form["inflight_entertainment"])
            baggage_handling = int(request.form["baggage_handling"])
            cleanliness = int(request.form["cleanliness"])
            departure_delay = int(request.form["departure_delay"])
            arrival_delay = int(request.form["arrival_delay"])
            gender = int(request.form["gender"])
            customer_type = int(request.form["customer_type"])
            travel_type = int(request.form["type_of_travel"])
            class_Type = request.form["Class"]

            Class_Eco = 0
            Class_Eco_Plus = 0
            if class_Type == 'ECO':
                Class_Eco = 1
            elif class_Type == 'ECO_PLUS':
                Class_Eco_Plus = 1

            UNSEEN_DATA = [[age, flight_distance, inflight_entertainment, baggage_handling,
                           cleanliness, departure_delay, arrival_delay, gender,
                           customer_type, travel_type, Class_Eco, Class_Eco_Plus]]

            prediction = model.predict(UNSEEN_DATA)[0]
            labels = {'1': "SATISFIED", '0': "DISSATISFIED"}

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
                class_type=class_Type,
                travel_type='Personal Travel' if travel_type == 1 else 'Business Travel'
            )

        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
