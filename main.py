from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(
    title="NFC AI Networking Card",
    description="A tap-powered experiment connecting humans and AI at DevFest 2025",
    version="1.0.0",
)

#Mount static directory for serving .vcf and future assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Include main API routes
app.include_router(router)
