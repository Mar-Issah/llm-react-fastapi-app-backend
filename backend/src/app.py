from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes are located in the api folder
from .api import challenge, webhooks

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(challenge.router, prefix="/api")
app.include_router(webhooks.router, prefix="/webhooks")
