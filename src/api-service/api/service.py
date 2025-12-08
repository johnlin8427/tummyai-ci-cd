"""
API service
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import user_list, user_photo, food_model, meal_history, health_report, chat_assistant

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


app.include_router(user_list.router, prefix="/user-list")
app.include_router(user_photo.router, prefix="/user-photo")
app.include_router(food_model.router, prefix="/food-model")
app.include_router(meal_history.router, prefix="/meal-history")
app.include_router(health_report.router, prefix="/health-report")
app.include_router(chat_assistant.router, prefix="/chat-assistant")
