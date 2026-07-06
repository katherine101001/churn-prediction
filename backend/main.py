from fastapi import FastAPI
from pydantic import BaseModel
import joblib, pandas as pd

app = FastAPI()
model = joblib.load('churn_model.joblib')

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
