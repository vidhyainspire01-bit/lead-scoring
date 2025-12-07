from fastapi import FastAPI
from .api import leads, scoring

app = FastAPI()

app.include_router(leads.router)
app.include_router(scoring.router)
