from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

data = pd.DataFrame({
    "age": [20,10,5,15,8],
    "severity": [5,4,2,5,3],
    "urgency": [1,0,0,1,0],
    "score": [85,60,35,90,50]
})

X = data[["age","severity","urgency"]]
y = data["score"]

model = LinearRegression()
model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))
print("JustiChain model successfull");