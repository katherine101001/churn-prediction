from fastapi import FastAPI
from pydantic import BaseModel
import joblib, pandas as pd

app = FastAPI()

import os

# 1. Get the exact folder path where main.py is currently sitting
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Glue that folder path together with the joblib filename
MODEL_PATH = os.path.join(BASE_DIR, 'churn_model.joblib')

# 3. Load the model safely using the full absolute path
model = joblib.load(MODEL_PATH)

class Customer(BaseModel):
    name: str
    tenure: int
    monthly_charges: float
    support_tickets: int
    annual_contract: int


@app.post("/predict")
def predict(c: Customer):
    cols = ["tenure", 'monthly_charges', 'support_tickets', 'annual_contract']
    X = pd.DataFrame([[c.tenure, c.monthly_charges,
                        c.support_tickets, c.annual_contract]], columns=cols)
    prob = float(model.predict_proba(X)[0, 1])
    return {"name": c.name, "churn_probability": round(prob, 3)}
