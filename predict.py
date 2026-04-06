import pickle

# load model
model = pickle.load(open("model.pkl", "rb"))

# example input: age, severity, urgency
input_data = [[25, 3, 1]]

prediction = model.predict(input_data)

print("Predicted score:", prediction[0])