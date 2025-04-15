from flask import Flask, render_template, request
from urllib.parse import quote_plus
from pymongo import MongoClient
import joblib

model = joblib.load("model2.pkl")

app = Flask(__name__)

username = "yash"
password = quote_plus("Yash@7940")  # This will encode the "@"

uri = f"mongodb+srv://{username}:{password}@cluster0.kqvitdh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client['studentdb']
collection = db['cgpa']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        extracurricular = request.form['extracurricular']
        previous_cgpa = float(request.form['cgpa'])
        attendance = float(request.form['attendance'])
        self_study = request.form['self_study']
        study_hours = float(request.form['study_hours'])

        input_data = {
            'Attendance': attendance,
            'StudyHours': study_hours,
            'PreviousCGPA': previous_cgpa,
            'Gender_Female': 1 if gender == 'female' else 0,
            'Gender_Male': 1 if gender == 'male' else 0,
            'ExtracurricularActivities_No': 1 if extracurricular == 'no' else 0,
            'ExtracurricularActivities_Yes': 1 if extracurricular == 'yes' else 0,
            'SelfStudy_No': 1 if self_study == 'no' else 0,
            'SelfStudy_Yes': 1 if self_study == 'yes' else 0
        }


        feature_order = ['Attendance', 'StudyHours', 'PreviousCGPA',
                        'Gender_Female', 'Gender_Male',
                        'ExtracurricularActivities_No', 'ExtracurricularActivities_Yes',
                        'SelfStudy_No', 'SelfStudy_Yes']
        input_features = [[input_data[feature] for feature in feature_order]]

        predicted_cgpa = model.predict(input_features)[0]

        collection.insert_one({**input_data, "predicted_cgpa": predicted_cgpa})

        return render_template("index.html", predicted_cgpa=round(predicted_cgpa, 2))

    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)
