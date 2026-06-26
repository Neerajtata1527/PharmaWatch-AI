from typing import List

from models.raw_article import RawArticle


# --------------------------------------------------
# Articles containing these keywords are immediately
# discarded before reaching the LLM.
# --------------------------------------------------

NOISE_KEYWORDS = {

    # Sports
    "football",
    "soccer",
    "cricket",
    "nba",
    "ipl",
    "fifa",
    "tennis",
    "golf",
    "olympics",
    "world cup",

    # Entertainment
    "movie",
    "movies",
    "film",
    "actor",
    "actress",
    "celebrity",
    "hollywood",
    "bollywood",
    "music",
    "concert",
    "album",
    "netflix",
    "marvel",
    "avatar",

    # Gaming
    "gaming",
    "xbox",
    "playstation",
    "nintendo",
    "steam",

    # Shopping / Deals
    "deal",
    "discount",
    "coupon",
    "sale",
    "prime day",
    "black friday",

    # Product Reviews
    "review",
    "benchmark",
    "driver",
    "firmware",
    "motherboard",
    "graphics card",
    "gpu",
    "cpu",

    # Misc
    "recipe",
    "fashion",
    "travel guide",
}


# --------------------------------------------------
# Articles containing these keywords are likely
# important for PharmaWatch.
# --------------------------------------------------

IMPORTANT_KEYWORDS = {

    # Geopolitics
    "war",
    "missile",
    "conflict",
    "attack",
    "military",
    "terror",
    "sanction",
    "embargo",

    # Shipping
    "shipping",
    "cargo",
    "port",
    "harbor",
    "vessel",
    "container",
    "logistics",
    "freight",
    "trade route",

    # Manufacturing
    "factory",
    "manufacturing",
    "production",
    "industrial",
    "plant",

    # Trade
    "trade",
    "export",
    "import",
    "tariff",

    # Infrastructure
    "airport",
    "rail",
    "bridge",
    "power",
    "pipeline",

    # Natural disasters
    "earthquake",
    "flood",
    "cyclone",
    "hurricane",
    "wildfire",
    "tsunami",
    "volcano",

    # Health
    "pandemic",
    "epidemic",
    "disease",

    # Energy
    "oil",
    "gas",
    "energy",

    # Pharma
    "pharmaceutical",
    "medicine",
    "drug",
    "api",
    "chemical",
}


# --------------------------------------------------
# Check whether article is obvious noise.
# --------------------------------------------------

def is_noise(article: RawArticle) -> bool:

    text = (
        f"{article.title} "
        f"{article.description}"
    ).lower()

    return any(
        keyword in text
        for keyword in NOISE_KEYWORDS
    )


# --------------------------------------------------
# Check whether article appears relevant for
# supply chain analysis.
# --------------------------------------------------

def is_potential_supply_chain_event(
    article: RawArticle,
) -> bool:

    text = (
        f"{article.title} "
        f"{article.description}"
    ).lower()

    return any(
        keyword in text
        for keyword in IMPORTANT_KEYWORDS
    )


# --------------------------------------------------
# Main filter used before Gemini.
# --------------------------------------------------

def filter_articles(
    articles: List[RawArticle],
) -> List[RawArticle]:

    filtered = []

    for article in articles:

        # Skip obvious junk
        if is_noise(article):
            continue

        # Keep articles that are likely useful
        if is_potential_supply_chain_event(article):
            filtered.append(article)

    return filtered