from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import leads, scoring

app = FastAPI(title="RAKEZ Lead Engine API")

# Allow Streamlit to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(leads.router, prefix="")
app.include_router(scoring.router, prefix="")

@app.get("/")
def root():
    return {"message": "RAKEZ Lead Engine API running"}
