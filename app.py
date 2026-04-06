from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

case_map = {
    "Civil": 0,
    "Criminal": 1,
    "Family/Matrimonial": 2,
    "Property": 3,
    "Bail": 4
}

@app.route("/")
def home():
    return render_template("index.html")   # 🔥 THIS LINE FIXES YOUR ISSUE

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_data = pd.DataFrame([{
        "age": float(data["age"]),
        "severity": float(data["severity"]),
        "urgency": float(data["urgency"])
    }])

    prediction = model.predict(input_data)[0]

    return jsonify({"prediction": float(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)