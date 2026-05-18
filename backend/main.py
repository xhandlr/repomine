from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.analyze import router as analyze_router
from .routes.jobs import router as jobs_router

app = FastAPI(title="repomine API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(jobs_router)
