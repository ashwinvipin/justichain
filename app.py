from flask import Flask, request, jsonify, render_template, redirect, session
import pickle
import pandas as pd
import secrets

# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

case_map = {
    "Civil": 0,
    "Criminal": 1,
    "Family/Matrimonial": 2,
    "Property": 3,
    "Bail": 4
}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # simple demo login (you can improve later)
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ---------------- HOME ----------------
@app.route("/")
def home():
    if not session.get("user"):
        return redirect("/login")
    return render_template("index.html")

# ---------------- PREDICT (SECURED) ----------------
@app.route("/predict", methods=["POST"])
def predict():
    # 🔒 Check login
    if not session.get("user"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json

    # 🔒 Validate input
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        age = float(data.get("age", 0))
        severity = float(data.get("severity", 0))
        urgency = float(data.get("urgency", 0))
    except:
        return jsonify({"error": "Invalid input format"}), 400

    # 🔒 Basic sanity checks
    if age < 0 or severity < 0 or urgency < 0:
        return jsonify({"error": "Invalid values"}), 400

    input_data = pd.DataFrame([{
        "age": age,
        "severity": severity,
        "urgency": urgency
    }])

    prediction = model.predict(input_data)[0]

    return jsonify({"prediction": float(prediction)})

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
