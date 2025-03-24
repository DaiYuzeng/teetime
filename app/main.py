from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base
from app.models import user
from app.routers import auth, user, teetime, signature

app = FastAPI()

# Allow requests from the frontend
origins = [
    "http://localhost:3000",  # Next.js local development
    "https://your-production-domain.com",  # Add production URL when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(teetime.router, prefix="/api", tags=["teetime"])
app.include_router(signature.router, prefix="/api", tags=["signature"])
