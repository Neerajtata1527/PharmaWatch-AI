import os

from dotenv import load_dotenv

load_dotenv()

# =====================================================
# API KEYS
# =====================================================

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")




# =====================================================
# NEWS API CONFIGURATION
# =====================================================

NEWS_QUERY = (
    "war OR shipping OR port OR sanctions "
    "OR export OR import OR factory "
    "OR earthquake OR flood "
    "OR strike OR infrastructure"
)

NEWS_LANGUAGE = "en"

NEWS_SORT_BY = "publishedAt"

NEWS_PAGE_SIZE = 20


# =====================================================
# HTTP CONFIGURATION
# =====================================================

REQUEST_TIMEOUT = 15.0


# =====================================================
# GDELT CONFIGURATION
# =====================================================

GDELT_BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

GDELT_QUERY = "war"

GDELT_TIMESPAN = "24h"

GDELT_MAX_RECORDS = 20

GDELT_MODE = "ArtList"

GDELT_FORMAT = "json"


# =====================================================
# LLM CONFIGURATION
# =====================================================

# Fast model for Event Agent
GROQ_MODEL = "llama-3.1-8b-instant"

# Better reasoning model (Research Agent later)
GROQ_REASONING_MODEL = "llama-3.3-70b-versatile"
