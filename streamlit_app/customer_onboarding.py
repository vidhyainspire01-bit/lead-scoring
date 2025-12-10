import streamlit as st
import requests

st.set_page_config(page_title="Lead Onboarding", layout="centered")

st.markdown("""
    <h2 style='text-align:center; color:#4E8EF7;'>RAKEZ Lead Onboarding Portal</h2>
    <p style='text-align:center; color:gray;'>Submit new customer leads for scoring</p>
""", unsafe_allow_html=True)

with st.form("lead_form"):
    st.markdown("📝 Customer Information")

    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name")
    email = col2.text_input("Email")

    col3, col4 = st.columns(2)
    phone = col3.text_input("Phone")
    country = col4.selectbox("Country", ["UAE", "India", "KSA", "Egypt", "UK", "USA"])

    industry = st.selectbox(
        "Industry",
        ["Real Estate", "Manufacturing", "Tech Startup", "Healthcare", "Consulting", "E-commerce"]
    )

    campaign = st.selectbox(
        "Campaign Source",
        ["Google Ads", "Expo Event", "Investor Webinar", "Email Marketing", "Referral"]
    )

    service = st.selectbox(
        "Service Interested In",
        ["Business Setup", "Visa Services", "Corporate Bank Account", "Office Leasing", "Licensing"]
    )

    budget = st.number_input("Estimated Budget (AED)", min_value=1000, step=1000)
    activity_score = st.slider("Activity / Engagement Score", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Submit Lead")

if submitted:
    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "country": country,
        "industry": industry,
        "campaign": campaign,
        "service": service,
        "budget": budget,
        "activity_score": activity_score
    }

    try:
        res = requests.post("http://localhost:8000/leads", json=payload)
        if res.status_code == 200:
            st.success("Lead created successfully!")
            lead = res.json()

            st.info(f"Lead ID: {lead['id']}")

            # Optional: Real-time scoring
            score_res = requests.post(f"http://localhost:8000/score/{lead['id']}")
            if score_res.status_code == 200:
                score_data = score_res.json()
                st.success(f"Lead Score: {score_data['score']} | Band: {score_data['band']}")

        else:
            st.error("Failed to create lead")

    except Exception as e:
        st.error(f"Error: {str(e)}")



# import streamlit as st
# import requests
# import pandas as pd

# st.set_page_config(page_title="RAKEZ Lead Onboarding", layout="wide")

# # Load Theme
# with open("theme.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # Header
# st.markdown("""
# <h1 style='text-align:center; color:#4E8EF7;'>RAKEZ Lead Onboarding Portal</h1>
# <p style='text-align:center; color:gray; font-size:18px;'>Submit new leads and trigger automated model scoring</p>
# """, unsafe_allow_html=True)

# st.markdown("<div class='card'>", unsafe_allow_html=True)

# st.subheader("📝 Customer Information")

# col1, col2 = st.columns(2)
# name = col1.text_input("Full Name")
# email = col2.text_input("Email")

# col3, col4 = st.columns(2)
# phone = col3.text_input("Phone Number")
# country = col4.selectbox("Country", ["UAE", "India", "Saudi Arabia", "UK", "USA"])

# industry = st.selectbox("Industry", [
#     "Real Estate", "Manufacturing", "Tech Startup",
#     "Healthcare", "Finance", "Consulting", "E-commerce"
# ])

# campaign = st.selectbox("Campaign Source", [
#     "Google Ads", "Facebook Ads", "LinkedIn", "Referral", "Expo Event"
# ])

# service = st.selectbox("Service Interested In", [
#     "Business Setup", "Visa Services", "Office Leasing",
#     "Banking Support", "Logistics"
# ])

# col5, col6 = st.columns(2)
# budget = col5.number_input("Estimated Budget (AED)", min_value=5000, step=1000)
# activity_score = col6.slider("Engagement Score", 0.0, 1.0, 0.5)

# st.markdown("</div>", unsafe_allow_html=True)

# if st.button("🚀 Submit Lead"):
#     payload = {
#         "name": name, "email": email, "phone": phone, "country": country,
#         "industry": industry, "campaign": campaign, "service": service,
#         "budget": budget, "activity_score": activity_score
#     }

#     resp = requests.post("http://localhost:8000/leads", json=payload)

#     if resp.status_code == 200:
#         lead = resp.json()
#         lead_id = lead["id"]
#         st.success(f"Lead Created: ID {lead_id}")

#         # Auto-score
#         score_resp = requests.post(f"http://localhost:8000/score/{lead_id}")

#         if score_resp.status_code == 200:
#             score_data = score_resp.json()
#             st.success(f"🎯 Lead Score: {score_data['score']} | Band: {score_data['band']}")
#         else:
#             st.error("Scoring failed.")
#     else:
#         st.error("Lead creation failed.")
# st.markdown("Data Source: RAKEZ Lead Engine API")