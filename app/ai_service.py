import google.generativeai as genai
import random
from app.config import settings

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)

def generate_ai_fact():
    """
    Generates a concise, unique AI fun fact about how Google uses AI
    in real products or research.
    Prioritizes instant response time — no retry delays.
    Falls back gracefully to Gemini Lite without user-visible lag.
    """

    # Slight variation to dodge caching or reuse on Gemini’s backend
    variation_hint = random.randint(1000, 9999)
    prompt = (
        f"Provide one concise AI fun fact (≤25 words) "
        f"about how Google uses AI in real products, research, or tools. "
        f"Make it fresh and distinct. Seed reference: {variation_hint}"
    )

    config = {
        "temperature": 0.8,          # keeps it creative but stable
        "max_output_tokens": 60,     # short, clean responses
    }

    try:
        # Primary fast model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt, generation_config=config)

        if response and hasattr(response, "text") and response.text.strip():
            return response.text.strip()

        raise ValueError("Empty primary response")

    except Exception:
        # Silent fallback — user never sees failure tag
        try:
            fallback_model = genai.GenerativeModel("gemini-2.5-flash-lite")
            fallback_response = fallback_model.generate_content(prompt, generation_config=config)

            if fallback_response and hasattr(fallback_response, "text") and fallback_response.text.strip():
                return fallback_response.text.strip()
            else:
                raise ValueError("Empty fallback response")

        except Exception:
            # Last-resort default message (rare)
            return "Google uses AI to improve products like Search, Photos, and Translate with real-time intelligence."

#Hi friend