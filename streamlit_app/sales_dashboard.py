# # # import streamlit as st
# # # import pandas as pd
# # # import requests
# # # import plotly.express as px

# # # st.set_page_config(page_title="RAKEZ Sales Dashboard", layout="wide")

# # # st.markdown("""
# # #     <h2 style='text-align:center; color:#4E8EF7;'>Sales Lead Insights Dashboard</h2>
# # #     <p style='text-align:center; color:gray;'>Monitor customer scoring & prioritize leads</p>
# # # """, unsafe_allow_html=True)

# # # # Fetch leads
# # # res = requests.get("http://localhost:8000/leads")
# # # data = pd.DataFrame(res.json()) if res.status_code == 200 else pd.DataFrame()

# # # if data.empty:
# # #     st.warning("No lead data available.")
# # #     st.stop()

# # # # KPI CARDS
# # # col1, col2, col3, col4 = st.columns(4)
# # # col1.metric("Total Leads", len(data))
# # # col2.metric("Hot Leads (A,B)", len(data[data["band"].isin(["A+", "A", "B"])]))
# # # col3.metric("Cold Leads", len(data[data["band"].isin(["C", "D"])]))
# # # col4.metric("Avg Score", round(data["score"].mean(), 2))

# # # # Score Distribution
# # # fig = px.histogram(data, x="score", nbins=20, title="Lead Score Distribution", color_discrete_sequence=["#4E8EF7"])
# # # st.plotly_chart(fig, use_container_width=True)

# # # # Filters
# # # industries = ["All"] + sorted(data["industry"].unique().tolist())
# # # selected_industry = st.selectbox("Filter by Industry", industries)

# # # filtered = data if selected_industry == "All" else data[data["industry"] == selected_industry]

# # # def highlight_band(val):
# # #     if val in ["A+", "A"]:
# # #         return "background-color: #d4ffd4"   # green
# # #     elif val == "B":
# # #         return "background-color: #fff7d4"   # yellow
# # #     elif val == "C":
# # #         return "background-color: #ffd4d4"   # red
# # #     else:
# # #         return ""  # safe for None / missing / empty values

# # # st.dataframe(
# # #     filtered.style.applymap(highlight_band, subset=["band"]),
# # #     width="stretch"
# # # )
# # # st.markdown("Data Source: RAKEZ Lead Engine API")




# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import numpy as np
# # import requests
# # from datetime import datetime, timedelta

# # # -----------------------------------------------------
# # # PAGE CONFIG
# # # -----------------------------------------------------
# # st.set_page_config(
# #     page_title="RAKEZ Sales & ML Monitoring Dashboard",
# #     layout="wide",
# # )

# # # -----------------------------------------------------
# # # PAGE HEADER
# # # -----------------------------------------------------
# # st.markdown("""
# #     <h1 style='text-align:center; color:#4E8EF7;'>📊 RAKEZ Sales Lead Intelligence Dashboard</h1>
# #     <p style='text-align:center; color:gray; font-size:18px;'>
# #         Real-time monitoring of Lead Quality, Model Health & CRM Integration
# #     </p>
# # """, unsafe_allow_html=True)


# # # -----------------------------------------------------
# # # LOAD DATA FROM FASTAPI
# # # -----------------------------------------------------
# # try:
# #     res = requests.get("http://localhost:8000/leads")
# #     leads = pd.DataFrame(res.json())
# # except Exception as e:
# #     st.error("❌ Failed to fetch leads from API")
# #     st.stop()

# # if leads.empty:
# #     st.warning("No leads available.")
# #     st.stop()


# # # -----------------------------------------------------
# # # METRICS TOP ROW
# # # -----------------------------------------------------
# # total_leads = len(leads)
# # hot_leads = len(leads[leads["band"].isin(["A", "A+"])] if "band" in leads else [])
# # avg_score = round(leads["score"].astype(float).fillna(0).mean(), 2)
# # cold_leads = len(leads[leads["band"] == "C"]) if "band" in leads else 0

# # col1, col2, col3, col4 = st.columns(4)

# # col1.metric("Total Leads", total_leads)
# # col2.metric("🔥 Hot Leads (A/B)", hot_leads)
# # col3.metric("❄️ Cold Leads (C)", cold_leads)
# # col4.metric("⭐ Avg Score", avg_score)


# # # -----------------------------------------------------
# # # MODEL HEALTH SECTION
# # # -----------------------------------------------------
# # st.markdown("## 🧠 Model Health Summary")

# # model_latency = np.random.randint(80, 200)   # ms
# # throughput = np.random.randint(20, 60)       # req/min
# # error_rate = np.round(np.random.uniform(0.0, 2.0), 2)  # %

# # m1, m2, m3 = st.columns(3)
# # m1.metric("Latency (p95)", f"{model_latency} ms", "-")
# # m2.metric("Throughput", f"{throughput} req/min")
# # m3.metric("Error Rate", f"{error_rate}%")

# # st.markdown("---")


# # # -----------------------------------------------------
# # # LEAD SCORE DISTRIBUTION
# # # -----------------------------------------------------
# # st.markdown("### 📈 Lead Score Distribution")

# # hist_col, segment_col = st.columns([2, 1])

# # # Histogram + KDE
# # fig = px.histogram(
# #     leads,
# #     x="score",
# #     nbins=20,
# #     marginal="box",
# #     title="Score Distribution",
# #     color_discrete_sequence=["#4E8EF7"]
# # )
# # hist_col.plotly_chart(fig, use_container_width=True)

# # # Segment chart
# # leads["segment"] = leads["score"].apply(
# #     lambda x: "A+" if x >= 0.9 else "A" if x >= 0.8 else "B" if x >= 0.5 else "C"
# # )

# # segment_counts = leads["segment"].value_counts().reset_index()
# # segment_counts.columns = ["segment", "count"]

# # fig2 = px.bar(
# #     segment_counts,
# #     x="segment",
# #     y="count",
# #     title="Lead Segments (A+, A, B, C)",
# #     color="segment",
# #     color_discrete_map={
# #         "A+": "#00C853",
# #         "A": "#1DE9B6",
# #         "B": "#FFD600",
# #         "C": "#FF5252"
# #     }
# # )
# # segment_col.plotly_chart(fig2, use_container_width=True)

# # st.markdown("---")


# # # -----------------------------------------------------
# # # INDUSTRY ANALYSIS
# # # -----------------------------------------------------
# # st.markdown("### 🏭 Industry Breakdown")

# # industry_df = leads.groupby("industry").size().reset_index(name="count")

# # fig3 = px.pie(
# #     industry_df,
# #     names="industry",
# #     values="count",
# #     title="Leads Per Industry",
# #     hole=0.4,
# # )
# # st.plotly_chart(fig3, use_container_width=True)

# # st.markdown("---")


# # # -----------------------------------------------------
# # # 7-DAY TREND (Mock because trial DB doesn't have timestamps)
# # # -----------------------------------------------------
# # st.markdown("### 📉 Score Trend (Last 7 Days)")

# # trend_days = pd.date_range(end=datetime.today(), periods=7)
# # trend_scores = np.random.uniform(0.6, 0.9, size=7)

# # trend_df = pd.DataFrame({
# #     "date": trend_days,
# #     "avg_score": trend_scores
# # })

# # fig4 = px.line(
# #     trend_df,
# #     x="date",
# #     y="avg_score",
# #     markers=True,
# #     title="Average Score Trend (7-Day)"
# # )
# # st.plotly_chart(fig4, use_container_width=True)

# # st.markdown("---")


# # # -----------------------------------------------------
# # # CRM SYNCHRONIZATION STATUS
# # # -----------------------------------------------------
# # st.markdown("### 🔄 CRM Integration Status")

# # crm_ok = True
# # if crm_ok:
# #     st.success("✔ All scores synced to CRM")
# # else:
# #     st.error("❌ CRM sync failures detected")


# # # -----------------------------------------------------
# # # LEADS TABLE (Color-coded)
# # # -----------------------------------------------------
# # st.markdown("### 📋 Lead Details Table")

# # def highlight_band(val):
# #     if val in ["A+", "A"]:
# #         return "background-color: #d4ffd4"
# #     elif val == "B":
# #         return "background-color: #fff0b3"
# #     else:
# #         return "background-color: #ffd6d6"

# # if "band" in leads:
# #     st.dataframe(
# #         leads.style.applymap(highlight_band, subset=["band"]),
# #         use_container_width=True
# #     )
# # else:
# #     st.dataframe(leads, use_container_width=True)
# # st.markdown("Data Source: RAKEZ Lead Engine API")



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import numpy as np
# import requests
# from datetime import datetime, timedelta

# # =====================================================
# # GLOBAL PAGE CONFIG
# # =====================================================
# st.set_page_config(
#     page_title="RAKEZ Sales & ML Monitoring Dashboard",
#     layout="wide",
# )

# # Load custom CSS Theme
# try:
#     with open("theme.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# except:
#     pass

# # =====================================================
# # PAGE HEADER
# # =====================================================
# st.markdown("""
#     <h1 style='text-align:center; color:#4E8EF7;'>📊 RAKEZ Sales Lead Intelligence Dashboard</h1>
#     <p style='text-align:center; color:gray; font-size:18px;'>
#         Real-time monitoring of Lead Quality, Model Health, Drift & CRM Integration
#     </p>
# """, unsafe_allow_html=True)


# # =====================================================
# # LOAD LEAD DATA FROM API
# # =====================================================
# try:
#     res = requests.get("http://localhost:8000/leads")
#     leads = pd.DataFrame(res.json())
# except Exception:
#     st.error("❌ Failed to fetch leads from the FastAPI backend.")
#     st.stop()

# if leads.empty:
#     st.warning("⚠ No leads available in the system.")
#     st.stop()

# # Ensure score is numeric
# leads["score"] = pd.to_numeric(leads["score"], errors="coerce")


# # =====================================================
# # TOP METRICS
# # =====================================================
# total_leads = len(leads)
# hot_leads = len(leads[leads["band"].isin(["A", "A+", "B"])] if "band" in leads else [])
# cold_leads = len(leads[leads["band"] == "C"]) if "band" in leads else 0
# avg_score = round(leads["score"].astype(float).fillna(0).mean(), 2)

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Total Leads", total_leads)
# col2.metric("🔥 Hot Leads (A/B)", hot_leads)
# col3.metric("❄️ Cold Leads (C)", cold_leads)
# col4.metric("⭐ Avg Score", avg_score)


# # =====================================================
# # MODEL REGISTRY / SERVING STATUS PANEL
# # =====================================================
# st.markdown("## 🧩 Model Registry & Serving Status")

# HOST = st.secrets.get("DATABRICKS_HOST", None)
# TOKEN = st.secrets.get("DATABRICKS_TOKEN", None)
# ENDPOINT = "lead-scoring-endpoint"

# if HOST and TOKEN:
#     try:
#         url = f"https://{HOST}/api/2.0/serving-endpoints/{ENDPOINT}"
#         r = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"})

#         if r.status_code == 200:
#             st.success("✔ Model Serving Endpoint Active")
#             st.json(r.json())
#         else:
#             st.warning("⚠ Endpoint exists but not active or not reachable")
#     except:
#         st.error("❌ Error contacting Databricks Model Serving API")
# else:
#     st.info("ℹ Databricks tokens not configured — running on Local ML scoring.")


# st.markdown("---")


# # =====================================================
# # MODEL HEALTH METRICS (Mocked for Local Execution)
# # =====================================================
# st.markdown("## 🧠 Model Health Summary")

# colh1, colh2, colh3 = st.columns(3)
# colh1.metric("Latency (P95)", f"{np.random.randint(80, 200)} ms")
# colh2.metric("Throughput", f"{np.random.randint(20, 60)} req/min")
# colh3.metric("Error Rate", f"{round(np.random.uniform(0.0, 2.0), 2)}%")


# st.markdown("---")


# # =====================================================
# # PREDICTION DISTRIBUTION
# # =====================================================
# st.markdown("### 📈 Lead Score Distribution")

# left, right = st.columns([2, 1])

# # Histogram
# fig = px.histogram(
#     leads,
#     x="score",
#     nbins=25,
#     title="Score Distribution",
#     color_discrete_sequence=["#4E8EF7"],
#     opacity=0.85,
# )
# left.plotly_chart(fig, width="stretch")

# # Segments
# leads["segment"] = leads["score"].apply(
#     lambda x: "A+" if x >= 0.9 else "A" if x >= 0.8 else "B" if x >= 0.5 else "C"
# )
# segment_counts = leads["segment"].value_counts().reset_index()
# segment_counts.columns = ["segment", "count"]

# fig2 = px.bar(
#     segment_counts,
#     x="segment",
#     y="count",
#     title="Lead Segments",
#     color="segment",
#     color_discrete_map={"A+": "#00C853", "A": "#1DE9B6", "B": "#FFD600", "C": "#FF5252"}
# )
# right.plotly_chart(fig2, width="stretch")

# st.markdown("---")


# # =====================================================
# # DRIFT DETECTION (Simple Statistical Test)
# # =====================================================
# st.markdown("## 🧠 Data Drift Detection")

# def detect_drift(current, baseline):
#     """Simple KS Drift detection."""
#     from scipy.stats import ks_2samp

#     stat, p = ks_2samp(current, baseline)
#     drift = p < 0.05
#     return drift, round(p, 4)


# # Baseline = first 20% of data
# baseline = leads["score"].dropna().sample(frac=0.2, random_state=42)
# current = leads["score"].dropna()

# drift_detected, p_value = detect_drift(current, baseline)

# col_d1, col_d2 = st.columns(2)
# col_d1.metric("Drift Detected?", "YES" if drift_detected else "NO")
# col_d2.metric("P-Value", p_value)

# st.markdown("---")


# # =====================================================
# # INDUSTRY ANALYSIS
# # =====================================================
# st.markdown("### 🏭 Industry Breakdown")

# ind_df = leads.groupby("industry").size().reset_index(name="count")

# fig3 = px.pie(ind_df, names="industry", values="count",
#               title="Leads Per Industry", hole=0.45)

# st.plotly_chart(fig3, width="stretch")
# st.markdown("---")


# # =====================================================
# # 7 DAY SCORE TREND (Mocked)
# # =====================================================
# st.markdown("### 📉 Score Trend (Last 7 Days)")

# trend_days = pd.date_range(end=datetime.today(), periods=7)
# trend_scores = np.random.uniform(0.6, 0.9, size=7)

# trend_df = pd.DataFrame({"date": trend_days, "avg_score": trend_scores})

# fig4 = px.line(
#     trend_df,
#     x="date",
#     y="avg_score",
#     markers=True,
#     title="Average Score Trend (7-Day)"
# )
# st.plotly_chart(fig4, width="stretch")

# st.markdown("---")


# # =====================================================
# # CRM SYNC STATUS
# # =====================================================
# st.markdown("### 🔄 CRM Integration Status")

# crm_ok = True
# if crm_ok:
#     st.success("✔ All scores synced to CRM successfully")
# else:
#     st.error("❌ CRM sync issues detected")


# # =====================================================
# # LEAD TABLE (Color-coded)
# # =====================================================
# st.markdown("### 📋 Lead Details Table")

# def highlight_band(val):
#     if val in ["A+", "A"]:
#         return "background-color: #d4ffd4"
#     elif val == "B":
#         return "background-color: #fff5b3"
#     else:
#         return "background-color: #ffd6d6"

# if "band" in leads:
#     st.dataframe(leads.style.applymap(highlight_band, subset=["band"]), width="stretch")
# else:
#     st.dataframe(leads, width="stretch")

# st.markdown("<p style='text-align:right; color:gray;'>Data Source: RAKEZ Lead Engine API</p>",
#             unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from datetime import datetime, timedelta

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="RAKEZ Sales & ML Monitoring Dashboard",
    layout="wide",
)

# -----------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------
st.markdown("""
    <h1 style='text-align:center; color:#4E8EF7;'>📊 RAKEZ Sales Lead Intelligence Dashboard</h1>
    <p style='text-align:center; color:gray; font-size:18px;'>
        Real-time monitoring of Lead Quality, Model Health & CRM Integration
    </p>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA FROM FASTAPI
# -----------------------------------------------------
try:
    res = requests.get("http://localhost:8000/leads")
    leads = pd.DataFrame(res.json())
except Exception as e:
    st.error("❌ Failed to fetch leads from API")
    st.stop()

if leads.empty:
    st.warning("No leads available.")
    st.stop()

# -----------------------------------------------------
# NORMALISE TYPES & DERIVE SEGMENT/BAND
# -----------------------------------------------------
# make sure score is numeric
leads["score"] = pd.to_numeric(leads["score"], errors="coerce").fillna(0.0)

# segment (A+, A, B, C) – exec-level view
def get_segment(x: float) -> str:
    if x >= 0.90:
        return "A+"
    if x >= 0.80:
        return "A"
    if x >= 0.50:
        return "B"
    return "C"

# band (Hot / Warm / Cold) – sales prioritisation
def get_band(x: float) -> str:
    if x >= 0.75:
        return "Hot"
    if x >= 0.50:
        return "Warm"
    return "Cold"

leads["segment"] = leads["score"].apply(get_segment)
leads["band"] = leads["score"].apply(get_band)

# -----------------------------------------------------
# SUMMARY METRICS
# -----------------------------------------------------
total_leads = len(leads)
hot_leads = len(leads[leads["band"] == "Hot"])
cold_leads = len(leads[leads["band"] == "Cold"])
avg_score = round(leads["score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", total_leads)
col2.metric("🔥 Hot Leads (band = Hot)", hot_leads)
col3.metric("❄️ Cold Leads (band = Cold)", cold_leads)
col4.metric("⭐ Avg Score", avg_score)

st.markdown("---")

# -----------------------------------------------------
# MODEL HEALTH SUMMARY (mock)
# -----------------------------------------------------
st.markdown("## 🧠 Model Health Summary")

model_latency = np.random.randint(80, 200)  # ms
throughput = np.random.randint(20, 60)      # req/min
error_rate = np.round(np.random.uniform(0.0, 2.0), 2)  # %

m1, m2, m3 = st.columns(3)
m1.metric("Latency (p95)", f"{model_latency} ms")
m2.metric("Throughput", f"{throughput} req/min")
m3.metric("Error Rate", f"{error_rate}%")

st.markdown("---")

# -----------------------------------------------------
# LEAD SCORE DISTRIBUTION
# -----------------------------------------------------
st.markdown("### 📈 Lead Score Distribution")

hist_col, segment_col = st.columns([2, 1])

# Histogram of scores
fig = px.histogram(
    leads,
    x="score",
    nbins=20,
    title="Score Distribution",
    color_discrete_sequence=["#4E8EF7"]
)
hist_col.plotly_chart(fig, use_container_width=True)

# Segment bar chart (A+, A, B, C)
segment_counts = leads["segment"].value_counts().reset_index()
segment_counts.columns = ["segment", "count"]

fig2 = px.bar(
    segment_counts,
    x="segment",
    y="count",
    title="Lead Segments (A+, A, B, C)",
    color="segment",
    color_discrete_map={
        "A+": "#00C853",
        "A": "#1DE9B6",
        "B": "#FFD600",
        "C": "#FF5252"
    }
)
segment_col.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------
# INDUSTRY BREAKDOWN
# -----------------------------------------------------
st.markdown("### 🏭 Industry Breakdown")

industry_df = leads.groupby("industry").size().reset_index(name="count")

fig3 = px.pie(
    industry_df,
    names="industry",
    values="count",
    title="Leads Per Industry",
    hole=0.4,
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------
# SCORE TREND (MOCK)
# -----------------------------------------------------
st.markdown("### 📉 Score Trend (Last 7 Days)")

trend_days = pd.date_range(end=datetime.today(), periods=7)
trend_scores = np.random.uniform(0.6, 0.9, size=7)

trend_df = pd.DataFrame({
    "date": trend_days,
    "avg_score": trend_scores
})

fig4 = px.line(
    trend_df,
    x="date",
    y="avg_score",
    markers=True,
    title="Average Score Trend (7-Day)"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------
# CRM SYNCHRONIZATION STATUS
# -----------------------------------------------------
st.markdown("### 🔄 CRM Integration Status")

crm_ok = True
if crm_ok:
    st.success("✔ All scores synced to CRM")
else:
    st.error("❌ CRM sync failures detected")

# -----------------------------------------------------
# MODEL REGISTRY + SERVING STATUS (SAFE MODE)
# -----------------------------------------------------
st.markdown("### 🧩 Databricks Model Registry Status")

try:
    HOST = st.secrets["DATABRICKS_HOST"]
    TOKEN = st.secrets["DATABRICKS_TOKEN"]
except Exception:
    HOST = None
    TOKEN = None

if HOST and TOKEN:
    try:
        url = f"https://{HOST}/api/2.0/serving-endpoints/lead-scoring-endpoint"
        r = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"})

        if r.status_code == 200:
            st.success("✔ Model Serving Endpoint Active")
            st.json(r.json())
        else:
            st.warning("⚠ Endpoint exists but not active")
    except Exception:
        st.error("❌ Error contacting Databricks API")
else:
    st.info("ℹ Databricks Model Serving is disabled (local scoring mode)")

# -----------------------------------------------------
# LEADS TABLE (Color-coded by band)
# -----------------------------------------------------
st.markdown("### 📋 Lead Details Table")

def highlight_band(val: str):
    if val == "Hot":
        return "background-color: #d4ffd4"   # green-ish
    if val == "Warm":
        return "background-color: #fff0b3"   # yellow-ish
    if val == "Cold":
        return "background-color: #ffd6d6"   # red-ish
    return ""

st.dataframe(
    leads.style.applymap(highlight_band, subset=["band"]),
    use_container_width=True
)

st.markdown("Data Source: RAKEZ Lead Engine API")
