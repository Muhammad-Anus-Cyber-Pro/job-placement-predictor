from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
data = pd.read_csv('placement.csv')
# model load
model = pickle.load(open('placement.pkl','rb'))

@app.route('/')
def index():
    gender_raw = data['gender'].unique()
    gender = [
        {"value":g, "label":"Male" if g == "M" else "Female"}
        for g in gender_raw
    ]

    def format_category(values,mapping=None):
        return [
            {"value":v,"label":mapping[v] if mapping and v in mapping else v}
            for v in values
        ]

    ssc_board = data['ssc_board'].unique()
    hsc_board = data['hsc_board'].unique()
    hsc_subject = data['hsc_subject'].unique()
    undergrad_degree = format_category(data['undergrad_degree'].unique(),
                                       {
                                           "Sci&Tech":"Science & Technology",
                                           "Comm&Mgmt":"Commerce & Management",
                                           "Others":"Others"
                                       })
    work_experience	 = data['work_experience'].unique()
    specialisation = format_category(data['specialisation'].unique(),
                                     {
                                         "Mkt&HR":"Marketing & Human Resources",
                                         "Mkt&Fin":"Marketing & Finance"
                                     })
    return render_template('index.html',gender=gender,ssc_board=ssc_board,hsc_board=hsc_board,hsc_subject=hsc_subject,undergrad_degree=undergrad_degree,work_experience=work_experience,specialisation=specialisation)

@app.route('/predict',methods=['POST'])
def predict():
    data = request.form

    gender = data['gender']
    ssc_percentage = float(data['ssc_percentage'])
    ssc_board = data['ssc_board']
    hsc_percentage = float(data['hsc_percentage'])
    hsc_board = data['hsc_board']
    hsc_subject = data['hsc_subject']
    degree_percentage = float(data['degree_percentage'])
    undergrad_degree =  data['undergrad_degree']
    work_experience = data['work_experience']
    emp_test_percentage = float(data['emp_test_percentage'])
    specialisation = data['specialisation']
    mba_percent = float(data['mba_percent'])

    input_data = pd.DataFrame([[gender,ssc_percentage,ssc_board,hsc_percentage,hsc_board,hsc_subject,degree_percentage,undergrad_degree,work_experience,emp_test_percentage,specialisation,mba_percent]],columns=['gender','ssc_percentage','ssc_board','hsc_percentage','hsc_board','hsc_subject','degree_percentage','undergrad_degree','work_experience','emp_test_percentage','specialisation','mba_percent'])
    prediction = model.predict(input_data)[0]
    result = "Placed ✅" if prediction == 1 else "Not Placed ❎"
    return result


if __name__ == "__main__":
    app.run(debug=True)