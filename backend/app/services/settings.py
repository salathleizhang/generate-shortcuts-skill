from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = REPO_ROOT / "backend"
JOBS_ROOT = BACKEND_ROOT / "tmp" / "jobs"

try:
    from dotenv import load_dotenv

    load_dotenv(BACKEND_ROOT / ".env")
except ImportError:
    pass

# App
APP_ENV = os.getenv("APP_ENV", "development")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5174")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Gemini / LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Signing
SHORTCUTS_SIGN_MODE = os.getenv("SIGNING_MODE", "anyone")

# Cloudflare
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_D1_DATABASE_ID = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "")

# Clerk
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "")

# Cloudflare R2 (S3-compatible)
R2_BUCKET = os.getenv("CLOUDFLARE_R2_BUCKET", "")
R2_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "")
R2_ENDPOINT = os.getenv("CLOUDFLARE_R2_ENDPOINT", "")
