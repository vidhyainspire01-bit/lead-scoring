import random

def score_lead(lead):
    score = (lead.activity_score or 0) * 0.6 + random.uniform(0, 40)
    return round(score, 2)

def band_from_score(score):
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 40:
        return "C"
    else:
        return "D"
def model_version():
    return "v1.0.0"