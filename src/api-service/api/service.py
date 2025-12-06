"""
API service
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import meal_history, health_report

# Setup FastAPI app
app = FastAPI(title="TummyAI App API Server", description="API Server for TummyAI App", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the TummyAI app!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(meal_history.router, prefix="/meal-history")
app.include_router(health_report.router, prefix="/health-report")
