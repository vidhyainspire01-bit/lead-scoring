import requests
import json
import os

def score_lead(lead):
    """
    Local ML scoring logic (simple demo scoring).
    Replace this with UC model scoring when workspace is upgraded.
    """
    score = 0.0

    # Activity score weighted 60%
    score += (lead.activity_score or 0) * 0.6

    # Budget weighted 40%
    score += ((lead.budget or 0) / 100000) * 0.4

    return round(min(score, 1.0), 2)


def band_from_score(score: float) -> str:
    if score >= 0.8:
        return "A"
    elif score >= 0.5:
        return "B"
    else:
        return "C"

# import mlflow
# import pandas as pd

# # Load model directly from Unity Catalog (Production alias)
# MODEL_URI = "models:/dbw_rakez_ml.rakez_mlops.lead_scoring_model@prod"

# # Load once at startup
# model = mlflow.pyfunc.load_model(MODEL_URI)

# def score_lead(lead):
#     """
#     Score a lead using the UC MLflow model.
#     """
#     df = pd.DataFrame([{
#         "name": lead.name,
#         "email": lead.email,
#         "phone": lead.phone,
#         "country": lead.country,
#         "industry": lead.industry,
#         "campaign": lead.campaign,
#         "service": lead.service,
#         "budget": lead.budget,
#         "activity_score": lead.activity_score
#     }])

#     prediction = model.predict(df)[0]
#     return float(prediction)

# def band_from_score(score: float) -> str:
#     if score >= 0.8:
#         return "A"
#     elif score >= 0.5:
#         return "B"
#     else:
#         return "C"
