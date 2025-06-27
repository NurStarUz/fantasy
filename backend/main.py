from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, teams, transfers, points, updater

app = FastAPI()

origins = ["*"]  # Frontend CORS uchun

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlar
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(transfers.router)
app.include_router(points.router)
app.include_router(updater.router)

@app.get("/")
def root():
    return {"msg": "Fantasy Football API is running"}
