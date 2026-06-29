from typing import List

from models.raw_article import RawArticle

# ==========================================================
# Hard Block List
# ==========================================================

NOISE_KEYWORDS = {

    # Sports
    "football", "soccer", "cricket", "nba", "ipl", "fifa",
    "tennis", "golf", "olympics", "world cup", "formula 1",
    "motogp", "wimbledon", "uefa",

    # Entertainment
    "movie", "movies", "film", "actor", "actress",
    "celebrity", "hollywood", "bollywood", "music",
    "concert", "album", "netflix", "marvel", "avatar",
    "tv series", "box office",

    # Gaming
    "gaming", "xbox", "playstation", "nintendo",
    "steam", "esports",

    # Shopping
    "discount", "deal", "coupon", "sale",
    "black friday", "prime day",

    # Reviews
    "review", "benchmark", "gpu", "cpu",
    "motherboard", "graphics card",
    "firmware", "driver",

    # Lifestyle
    "recipe", "fashion", "travel guide",
    "celeb", "wedding",

    # Finance noise
    "stock picks",
    "stocks we think twice about",
    "earnings preview",
    "quarterly results",
    "premium growth",
    "share price",
    "ipo",
    "mutual fund",

    # Crypto
    "bitcoin",
    "ethereum",
    "crypto",
    "token",
    "coin",
    "blockchain",
    "nft",
}

# ==========================================================
# Strong Supply Chain Keywords
# ==========================================================

IMPORTANT_KEYWORDS = {

    # Geopolitics
    "war",
    "conflict",
    "missile",
    "attack",
    "terror",
    "sanction",
    "embargo",
    "navy",
    "military",
    "border",

    # Shipping
    "shipping",
    "cargo",
    "container",
    "port",
    "harbor",
    "vessel",
    "freight",
    "logistics",
    "shipping lane",
    "trade route",
    "strait",
    "hormuz",
    "red sea",
    "suez",

    # Trade
    "trade",
    "tariff",
    "export",
    "import",
    "restriction",
    "quota",

    # Manufacturing
    "factory",
    "plant",
    "production",
    "manufacturing",
    "shutdown",
    "closure",
    "strike",

    # Raw Materials
    "chemical",
    "api",
    "active pharmaceutical ingredient",
    "rare earth",
    "lithium",
    "fertilizer",

    # Pharma
    "pharmaceutical",
    "drug",
    "medicine",
    "vaccine",
    "antibiotic",

    # Infrastructure
    "airport",
    "bridge",
    "pipeline",
    "power grid",
    "electricity",

    # Natural disasters
    "earthquake",
    "flood",
    "cyclone",
    "hurricane",
    "typhoon",
    "tsunami",
    "wildfire",
    "volcano",

    # Health
    "pandemic",
    "epidemic",
    "outbreak",

    # Energy
    "oil",
    "gas",
    "lng",
    "refinery",
    "energy",
}

# ==========================================================
# Strong Exclusion Rules
# ==========================================================

EXCLUDED_PHRASES = {

    "football club",
    "movie review",
    "album review",
    "celebrity news",
    "match report",
    "live score",
    "stock recommendation",
    "price target",
}

# ==========================================================
# Noise Detection
# ==========================================================

def is_noise(article: RawArticle) -> bool:

    text = (
        f"{article.title} "
        f"{article.description or ''}"
    ).lower()

    if any(
        phrase in text
        for phrase in EXCLUDED_PHRASES
    ):
        return True

    if any(
        keyword in text
        for keyword in NOISE_KEYWORDS
    ):
        return True

    return False


# ==========================================================
# Supply Chain Detection
# ==========================================================

def is_potential_supply_chain_event(
    article: RawArticle,
) -> bool:

    text = (
        f"{article.title} "
        f"{article.description or ''}"
    ).lower()

    score = 0

    for keyword in IMPORTANT_KEYWORDS:

        if keyword in text:
            score += 1

    return score >= 2


# ==========================================================
# Filter
# ==========================================================

def filter_articles(
    articles: List[RawArticle],
) -> List[RawArticle]:

    filtered = []

    seen_titles = set()

    for article in articles:

        if not article.title:
            continue

        title = article.title.lower().strip()

        if title in seen_titles:
            continue

        seen_titles.add(title)

        if is_noise(article):
            continue

        if is_potential_supply_chain_event(article):
            filtered.append(article)

    print(f"\nArticles after Noise Filter: {len(filtered)}")

    return filtered