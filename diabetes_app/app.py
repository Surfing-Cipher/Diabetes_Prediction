from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load('diabetes_prediction_model.joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    probability = None
    input_data = {}
    errors = {}

    if request.method == 'POST':
        try:
            # Map HTML form field names to model's expected field names
            field_mapping = {
                'pregnancies': 'Pregnancies',
                'glucose': 'Glucose',
                'bloodpressure': 'BloodPressure',
                'skinthickness': 'SkinThickness',
                'insulin': 'Insulin',
                'bmi': 'BMI',
                'diabetespedigreefunction': 'DiabetesPedigreeFunction',
                'age': 'Age'
            }

            # Extract form values and validate
            for form_field, model_field in field_mapping.items():
                value = request.form.get(form_field)
                input_data[form_field] = value

                if not value:
                    errors[form_field] = "This field is required."
                else:
                    try:
                        float(value)
                    except ValueError:
                        errors[form_field] = "Must be a number."

            # If no validation errors, make prediction
            if not errors:
                # Construct input for model using the model's expected feature names
                model_input = {
                    field_mapping[form_field]: float(input_data[form_field])
                    for form_field in field_mapping
                }

                input_df = pd.DataFrame([model_input])  # One-row DataFrame
                print("Model input columns:", input_df.columns.tolist())
                pred = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0][1]

                prediction = "Diabetes" if pred == 1 else "No Diabetes"
                probability = round(proba * 100, 2)

        except Exception as e:
            prediction = "Error: " + str(e)

    return render_template(
        'index.html',
        prediction=prediction,
        probability=probability,
        input_data=input_data,
        errors=errors
    )

if __name__ == '__main__':
    app.run(debug=True)
