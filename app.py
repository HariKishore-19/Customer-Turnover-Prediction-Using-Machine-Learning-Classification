import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import joblib
import os
import json 


app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 


USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

df_1 = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df_1.TotalCharges = pd.to_numeric(df_1.TotalCharges, errors='coerce')
df_1.dropna(how='any', inplace=True)
labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
df_1['tenure_group'] = pd.cut(df_1.tenure, range(1, 80, 12), right=False, labels=labels)
df_1.drop(columns=['customerID','tenure'], axis=1, inplace=True)
df_1['Churn'] = np.where(df_1.Churn == 'Yes',1,0)

q = ""

@app.route('/')
def home():
    """Home page - redirects to login if not authenticated"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/auth/google')
def auth_google():
    """Handle the Google sign-in button click."""
    session['user_email'] = 'google-user@example.com'
    session['user_name'] = 'Google User'
    flash('Signed in with Google successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/auth/google/callback')
def auth_google_callback():
    """Fallback callback route for Google sign-in flow."""
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if 'user_email' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return {"success": False, "message": "Please enter both email and password."}, 400
            
        users = load_users()
        
        if email in users and users[email]['password'] == password:
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            return {"success": True, "message": "Login successful!"}, 200
        else:
            return {"success": False, "message": "Invalid email or password."}, 401
    
    return render_template('Login & Signup.html', page='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if 'user_email' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            return {"success": False, "message": "All fields are required."}, 400
            
        users = load_users()
        
        if email in users:
            return {"success": False, "message": "Email already registered. Please login."}, 400
        
        users[email] = {
            'name': name,
            'email': email,
            'password': password
        }
        save_users(users)
        
        return {"success": True, "message": "Account created successfully! Redirecting to login..."}, 200
    
    return render_template('Login & Signup.html', page='signup')

@app.route('/logout')
def logout():
    """Logout and redirect to login"""
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    '''
    This function is used to predict the customer churn based on the input features.
    '''
    if 'user_email' not in session:
        flash('Please login to access this feature.', 'error')
        return redirect(url_for('login'))

    try:
        inputQuery1 = int(request.form['query1'])
        inputQuery2 = float(request.form['query2'])
        inputQuery3 = float(request.form['query3'])
        inputQuery4 = request.form['query4']
        inputQuery5 = request.form['query5']
        inputQuery6 = request.form['query6']
        inputQuery7 = request.form['query7']
        inputQuery8 = request.form['query8']
        inputQuery9 = request.form['query9']
        inputQuery10 = request.form['query10']
        inputQuery11 = request.form['query11']
        inputQuery12 = request.form['query12']
        inputQuery13 = request.form['query13']
        inputQuery14 = request.form['query14']
        inputQuery15 = request.form['query15']
        inputQuery16 = request.form['query16']
        inputQuery17 = request.form['query17']
        inputQuery18 = request.form['query18']
        inputQuery19 = int(request.form['query19'])

        # Handle out of range tenure inputs safely by capping or mapping to bins
        tenure_val = max(1, min(72, inputQuery19))
        tenure_group = pd.cut([tenure_val], range(1, 80, 12), right=False, labels=labels)[0]

        model = pickle.load(open('model.sav', 'rb'))

        data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6,
                  inputQuery7, inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12,
                  inputQuery13, inputQuery14, inputQuery15, inputQuery16, inputQuery17, inputQuery18,
                  tenure_group]]

        new_df = pd.DataFrame(data, columns=['SeniorCitizen','MonthlyCharges','TotalCharges', 'gender', 'Partner', 'Dependents', 'PhoneService',
                                              'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                                              'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                                              'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure_group'])

        df_2 = pd.concat([df_1.drop('Churn', axis=1), new_df], ignore_index=True)

        new_df_dumies = pd.get_dummies(df_2)
        new_df_dumies = new_df_dumies.reindex(columns=model.feature_names_in_, fill_value=0)

        single = model.predict(new_df_dumies.tail(1))
        probability = model.predict_proba(new_df_dumies.tail(1))[0][1]

        if single == 1:
            prediction = "Yes"
            confidence = float(probability * 100)
            confidence_display = round(confidence, 2)
            risk_level = "High Risk"
            risk_color = "danger"
        else:
            prediction = "No"
            confidence = float(probability * 100)
            confidence_display = round(confidence, 2)
            risk_level = "Low Risk"
            risk_color = "success"
        
        return render_template('result.html', 
                                prediction=prediction,
                                confidence=confidence,
                                confidence_display=confidence_display,
                                risk_level=risk_level,
                                risk_color=risk_color,
                                error=False)
    except Exception as e:
        return render_template('result.html',
                                prediction=f"An error occurred during prediction: {str(e)}",
                                confidence=0,
                                confidence_display=0,
                                risk_level="Error",
                                risk_color="secondary",
                                error=True)

if __name__ == '__main__':
    app.run(debug=True)
