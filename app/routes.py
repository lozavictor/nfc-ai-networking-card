from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.redis_client import redis_client
from app.ai_service import generate_ai_fact

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def root():
    """Root endpoint to verify API status."""
    return {"message": "NFC AI Networking Card is live!"}


@router.get("/tap", response_class=HTMLResponse)
def tap(request: Request):
    """
    NFC route:
    - Increments total tap count (Redis)
    - Generates a fresh AI fact from Gemini
    - Renders the interactive card template
    """
    try:
        #Increment Redis counter
        total_taps = redis_client.incr("tap_counter")

        #Generate AI fact
        fact = generate_ai_fact()
        ai_source = "Gemini 2.5 Flash"

        #Build context for Jinja2 template
        context = {
            "request": request,
            "session_id": total_taps,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "fact": fact,
            "source": ai_source,
            "name": "Victor Loza",
            "title": "Junior Back-End Developer",
            "email": "Loza.Victor@outlook.com",
            "linkedin": "https://linkedin.com/in/lozavictor",
            "github": "https://github.com/lozavictor",
        }

        return templates.TemplateResponse("card.html", context)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Tap route failed",
                "details": str(e),
                "hint": "Check Redis or Gemini API availability.",
            },
        )


@router.get("/stats")
def stats():
    """
    Fetch total tap statistics (Redis counter).
    Returns live total taps for operational tracking.
    """
    try:
        total_taps = redis_client.get("tap_counter")
        total_taps = int(total_taps) if total_taps else 0
        return {"total_taps": total_taps, "status": "Tracking active"}
    except Exception as e:
        return {"error": "Redis error", "details": str(e)}


@router.get("/fact")
def get_ai_fact():
    """
    Standalone endpoint to fetch AI-generated fact and source.
    Used API health checks and debugging Gemini output.
    """
    try:
        fact = generate_ai_fact()
        return {"fact": fact, "source": "Gemini 2.5 Flash"}
    except Exception as e:
        return {
            "error": "AI Generation failed",
            "details": str(e),
            "hint": "Verify Gemini API key or rate limits.",
        }

