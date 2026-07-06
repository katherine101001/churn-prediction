import streamlit as st, requests

N8N = "https://katherine2304.app.n8n.cloud/webhook/54827b0e-32f8-429f-83ee-7b8f55d81334"

st.title("Smart Customer Retention Assistant")
name = st.text_input("Customer Name", "Jane Tan")
tenure = st.slider("Tenure (months)", 1, 72, 6)
monthly = st.number_input("Monthly Charges (RM)", 20.0, 200.0, 95.0)
tickets = st.number_input("Support Tickets", 0, 20, 4)
contract = st.selectbox("Contract",["Month-to-month", "Annual"])

if st.button("Analyze & recommend"):
    payload = {"name": name, "tenure": tenure, "monthly_charges": monthly,
               "support_tickets": tickets, "annual_contract": 1 if contract=="Annual" else 0}
    d = requests.post(N8N, json=payload, timeout=60).json()
    st.metric("Churn Probability", f"{d['churn_probability']*100:.1f}%")
    
    st.write("n8n 返回的真实数据是：", d)
    st.subheader(f"Risk tier: {d['risk_tier']}")
    st.write(f"Offer: {d['recommended_offer']}")
    st.text_area("Draft message", d['draft_message'], height=1)