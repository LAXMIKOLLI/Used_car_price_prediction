# html guidance taken from github of  Animesh
# https://github.com/Animesh1911/Used-Car-Price-Prediction/commits?author=Animesh1911

from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
from datetime import datetime


app = Flask(__name__)

model = open('model_rf_reg.pkl', 'rb')  # loading our predicted model
regressor_model = pickle.load(model)
model.close()


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET","POST"])
@cross_origin()
def predict():
    # city
    NewDelhi = 0
    Mumbai = 0
    Bangalore = 0
    Chennai = 0
    Pune = 0
    Hyderabad = 0
    Noida = 0
    Gurgaon = 0
    Kolkata = 0
    Ahmedabad = 0

    # fuel type
    Diesel = 0
    PetrolLPG = 0
    Petrol = 0
    PetrolCNG = 0

    # TRANSMISSION
    Manual = 0
    Automatic = 0

    # insurance_type
    comprehensive = 0
    InsuranceExpired = 0
    NotAvailable = 0
    ThirdParty = 0
    ZeroDepreciation = 0

    if request.method == "POST":
        company_name = request.form['brand']

        model_name = request.form['Model']

        city = request.form['city']

        if city == 'Bangalore':
            Bangalore = 1
        elif city == 'Chennai':
            Chennai = 1
        elif city == 'Pune':
            Pune = 1
        elif city == 'Mumbai':
            Mumbai = 1
        elif city == 'Gurgaon':
            Gurgaon = 1
        elif city == 'Hyderabad':
            Hyderabad = 1
        elif city == 'Noida':
            Noida = 1
        elif city == 'Kolkata':
            Kolkata = 1
        elif city == 'NewDelhi':
            NewDelhi = 1
        else:
            Ahmedabad = 1

        fuel = request.form['fuel']

        if fuel == 'Diesel':
            Diesel = 1
        elif fuel == 'Petrol':
            Petrol = 1
        elif fuel == 'PetrolLPG':
            PetrolLPG = 1
        else:
            PetrolCNG = 1

        trans = request.form['Transmission']
        if trans == 'Manual':
            Manual = 1
        else:
            Automatic = 1

        Year = request.form['Year']
        car_life = datetime.now().year - int(Year)

        Kms = request.form['Kms']

        Owner = request.form['Owner']

        ins_type = request.form['insurance']
        if ins_type == comprehensive:
            comprehensive = 1
        elif ins_type == InsuranceExpired:
            InsuranceExpired = 1
        elif ins_type == NotAvailable:
            NotAvailable = 1
        elif ins_type == ThirdParty:
            ThirdParty = 1
        else:
            ZeroDepreciation = 1

        # prediction

        price = regressor_model.predict([[Kms, Owner, company_name, model_name, car_life, Petrol, PetrolCNG, PetrolLPG,
                                    Manual,InsuranceExpired, NotAvailable, ThirdParty, ZeroDepreciation, Bangalore,
                                    Chennai, Gurgaon, Hyderabad, Kolkata, Mumbai, NewDelhi, Noida, Pune]])

        output = round(price[0], 2)
        prediction_text = "Your estimated price of car is approximately Rs. {} lakhs. " \
                      "This price may change depending on the condition of the car.".format(output)

        return render_template("index.html", prediction_text=prediction_text)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
