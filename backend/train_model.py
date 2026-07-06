import numpy as np, pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier

np.random.seed(42); n = 100
tenure = np.random.randint(1, 72, n)
monthly = np.random.uniform(20, 120, n)
tickets = np.random.poisson(2, n)
contract = np.random.choice([0,1], n)
logit = -0.05*tenure + 0.02*monthly + 0.4*tickets + 1.5*contract - 1.0
churn = (np.random.rand(n) < (1/(1 + np.exp(-logit)))).astype(int)

X = pd.DataFrame({'tenure': tenure, 'monthly_charges': monthly,
                   'support_tickets': tickets, 'annual_contract': contract})

joblib.dump(RandomForestClassifier(n_estimators=100, random_state=42).fit(X, churn),
             'churn_model.joblib')