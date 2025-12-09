"""
API service
"""

import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import user_list, user_photo, food_model, meal_history, health_report, chat_assistant

# Set root_path based on environment
ROOT_PATH = os.getenv("ROOT_PATH", "")

# Setup FastAPI app
api_app = FastAPI(title="TummyAI App API Server", description="API Server for TummyAI App", version="v1")

# Enable CORSMiddleware
api_app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@api_app.get("/")
async def get_index():
    return {"message": "Welcome to the TummyAI app!"}


@api_app.get("/health")
async def health_check():
    return {"status": "healthy"}


api_app.include_router(user_list.router, prefix="/user-list")
api_app.include_router(user_photo.router, prefix="/user-photo")
api_app.include_router(food_model.router, prefix="/food-model")
api_app.include_router(meal_history.router, prefix="/meal-history")
api_app.include_router(health_report.router, prefix="/health-report")
api_app.include_router(chat_assistant.router, prefix="/chat-assistant")

# Mount your API under ROOT-PATH to match the Ingress rule
app = FastAPI(title="API Server", description="API Server", version="v1")
app.mount(ROOT_PATH, api_app)
