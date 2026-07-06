# import streamlit as st, requests

# N8N = "https://katherine2304.app.n8n.cloud/webhook/54827b0e-32f8-429f-83ee-7b8f55d81334"

# st.title("Smart Customer Retention Assistant")
# name = st.text_input("Customer Name", "Jane Tan")
# tenure = st.slider("Tenure (months)", 1, 72, 6)
# monthly = st.number_input("Monthly Charges (RM)", 20.0, 200.0, 95.0)
# tickets = st.number_input("Support Tickets", 0, 20, 4)
# contract = st.selectbox("Contract",["Month-to-month", "Annual"])

# if st.button("Analyze & recommend"):
#     payload = {"name": name, "tenure": tenure, "monthly_charges": monthly,
#                "support_tickets": tickets, "annual_contract": 1 if contract=="Annual" else 0}
#     st.metric("Churn Probability", f"{d['churn_probability']*100:.1f}%")
    
#     st.write("n8n 返回的真实数据是：", d)
#     st.subheader(f"Risk tier: {d['risk_tier']}")
#     st.write(f"Offer: {d['recommended_offer']}")
#     st.text_area("Draft message", d['draft_message'], height=1)

import streamlit as st
import requests

N8N = "https://katherine2304.app.n8n.cloud/webhook/54827b0e-32f8-429f-83ee-7b8f55d81334"

st.title("Smart Customer Retention Assistant")
name = st.text_input("Customer Name", "Jane Tan")
tenure = st.slider("Tenure (months)", 1, 72, 6)
monthly = st.number_input("Monthly Charges (RM)", 20.0, 200.0, 95.0)
tickets = st.number_input("Support Tickets", 0, 20, 4)
contract = st.selectbox("Contract", ["Month-to-month", "Annual"])

if st.button("Analyze & recommend"):
    payload = {
        "name": name, 
        "tenure": tenure, 
        "monthly_charges": monthly,
        "support_tickets": tickets, 
        "annual_contract": 1 if contract == "Annual" else 0
    }
    
    # 1. 正常发出请求并等待响应（不直接用 .json()）
    response = requests.post(N8N, json=payload, timeout=60)
    
    # 2. 如果状态码不是 200（代表 n8n 那边断了或者内部节点炸了）
    if response.status_code != 200:
        st.error(f"❌ n8n 自动化流返回了错误状态码: {response.status_code}")
        st.warning("以下是 n8n 返回的原始文本（我们可以根据这个直接揪出真正的凶手）：")
        st.code(response.text) # 👈 这一行会把底层的真实报错像照妖镜一样照在你的网页上
        st.stop() # 强制安全拦截，不让 Streamlit 继续往下走导致闪退
        
    # 3. 如果状态码是 200，我们再尝试转换为 JSON 字典
    try:
        d = response.json()
    except Exception as e:
        st.error("❌ 虽然状态码是 200，但返回的内容居然无法被解析为 JSON！")
        st.code(response.text)
        st.stop()

    # 4. 只有当上面顺利通过，才会执行数据展示，从此绝对不会再报红色闪退错误！
    st.metric("Churn Probability", f"{d.get('churn_probability', 0)*100:.1f}%")
    
    st.write("n8n 返回的真实数据是：", d)
    st.subheader(f"Risk tier: {d.get('risk_tier', 'Unknown')}")
    st.write(f"Offer: {d.get('recommended_offer', 'None')}")
    st.text_area("Draft message", d.get('draft_message', ''), height=1)