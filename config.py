import os
from pathlib import Path

from dotenv import load_dotenv

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

# =====================================================
# API KEYS
# =====================================================

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =====================================================
# DEDICATED KEYS FOR ALTERNATIVES AGENT
# =====================================================

TAVILY_API_KEY_ALTERNATIVES = (
    os.getenv("TAVILY_API_KEY_ALTERNATIVES")
    or TAVILY_API_KEY
)

GROQ_API_KEY_ALTERNATIVES = (
    os.getenv("GROQ_API_KEY_ALTERNATIVES")
    or GROQ_API_KEY
)

# =====================================================
# NEWS API
# =====================================================

NEWS_QUERY = (
    '('
    'war OR sanctions OR conflict OR strike '
    'OR "factory shutdown" '
    'OR "export ban" '
    'OR "shipping disruption" '
    'OR "port closure" '
    'OR earthquake '
    'OR flood '
    'OR wildfire '
    'OR hurricane '
    'OR cyclone'
    ') '
    'AND '
    '('
    'pharmaceutical '
    'OR pharma '
    'OR medicine '
    'OR drug '
    'OR API '
    'OR vaccine '
    'OR insulin '
    'OR biologics '
    'OR "supply chain"'
    ')'
)

NEWS_LANGUAGE = "en"
NEWS_SORT_BY = "publishedAt"
NEWS_PAGE_SIZE = 40

# =====================================================
# GDELT
# =====================================================

GDELT_BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

GDELT_QUERY = (
    '('
    'pharmaceutical '
    'OR medicine '
    'OR drug '
    'OR vaccine '
    'OR insulin '
    'OR biologics '
    'OR API '
    'OR "drug supply"'
    ') '
    'AND '
    '('
    'war '
    'OR sanctions '
    'OR conflict '
    'OR strike '
    'OR disruption '
    'OR shortage '
    'OR "factory shutdown" '
    'OR "export ban" '
    'OR earthquake '
    'OR flood '
    'OR wildfire '
    'OR cyclone'
    ')'
)

GDELT_TIMESPAN = "72h"
GDELT_MAX_RECORDS = 40
GDELT_MODE = "ArtList"
GDELT_FORMAT = "json"

# =====================================================
# HTTP
# =====================================================

REQUEST_TIMEOUT = 15.0

# =====================================================
# LLM
# =====================================================

GROQ_MODEL = "llama-3.1-8b-instant"

GROQ_REASONING_MODEL = (
    "llama-3.3-70b-versatile"
)

LLM_TEMPERATURE = 0

# =====================================================
# PARALLEL EXECUTION
# =====================================================

MAX_PARALLEL_WORKERS = 3

# =====================================================
# TAVILY
# =====================================================

TAVILY_MAX_RESULTS = 10
TAVILY_MIN_SCORE = 0.30
TAVILY_MAX_CONTENT_LENGTH = 800

# =====================================================
# RETRY
# =====================================================

MAX_RETRIES = 3
INITIAL_BACKOFF = 2
BACKOFF_MULTIPLIER = 2

# =====================================================
# DEBUG
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PharmaWatch AI Configuration")
    print("=" * 60)

    print(f"Base Directory : {BASE_DIR}")
    print(f".env Exists    : {ENV_FILE.exists()}")

    print()

    print(
        "NEWS_API_KEY             :",
        "Loaded" if NEWS_API_KEY else "Missing",
    )

    print(
        "GROQ_API_KEY             :",
        "Loaded" if GROQ_API_KEY else "Missing",
    )

    print(
        "TAVILY_API_KEY           :",
        "Loaded" if TAVILY_API_KEY else "Missing",
    )

    print()

    print(
        "Alternative Tavily Key   :",
        "Loaded" if TAVILY_API_KEY_ALTERNATIVES else "Missing",
    )

    print(
        "Alternative Groq Key     :",
        "Loaded" if GROQ_API_KEY_ALTERNATIVES else "Missing",
    )

    print()

    print(f"Workers                  : {MAX_PARALLEL_WORKERS}")
    print(f"Groq Model               : {GROQ_MODEL}")
    print(f"Tavily Results           : {TAVILY_MAX_RESULTS}")

    print("=" * 60)