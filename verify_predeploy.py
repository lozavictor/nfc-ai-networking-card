"""
verify_predeploy.py
Run this script before deploying to Render.
It checks:
- Redis connection
- Gemini API response
- Template path resolution
- Static .vcf file availability
"""

import os
import redis
import google.generativeai as genai
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# ---------------------------------------------------------------------
# Load ENVIRONMENT VARIABLES
# ---------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# Pull credentials
gemini_key = os.getenv("GEMINI_API_KEY")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

print("\n🚀 Starting Pre-Deployment Verification...\n")

# ---------------------------------------------------------------------
# 1️⃣ Redis Connectivity Check
# ---------------------------------------------------------------------
try:
    client = redis.from_url(redis_url, decode_responses=True)
    client.ping()
    print("✅ Redis Connection: SUCCESS")
except Exception as e:
    print(f"❌ Redis Connection FAILED → {e}")

# ---------------------------------------------------------------------
# 2️⃣ Gemini API Check
# ---------------------------------------------------------------------
try:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = "Provide a concise AI fun fact about how Google uses AI."
    response = model.generate_content(prompt)
    if response and hasattr(response, "text"):
        print(f"✅ Gemini AI Response: {response.text.strip()[:80]}...")
    else:
        raise ValueError("Empty or invalid Gemini response")
except Exception as e:
    print(f"❌ Gemini API FAILED → {e}")

# ---------------------------------------------------------------------
# 3️⃣ Template Rendering Path Check
# ---------------------------------------------------------------------
try:
    templates = Jinja2Templates(directory="app/templates")
    assert os.path.exists("app/templates/card.html")
    print("✅ Template Found: app/templates/card.html")
except Exception as e:
    print(f"❌ Template Check FAILED → {e}")

# ---------------------------------------------------------------------
# 4️⃣ Static File (.vcf) Check
# ---------------------------------------------------------------------
try:
    static_path = "app/static/victor_loza.vcf"
    assert os.path.exists(static_path)
    print(f"✅ Static VCF Found: {static_path}")
except Exception as e:
    print(f"❌ Static VCF Check FAILED → {e}")

# ---------------------------------------------------------------------
# ✅ FINAL STATUS
# ---------------------------------------------------------------------
print("\n🧾 Pre-deployment verification complete.\n")
print("If all items show ✅, your project is ready for Render deployment.\n")
