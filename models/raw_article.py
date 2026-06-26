from pydantic import BaseModel

class RawArticle(BaseModel):

    title: str

    description: str | None = ""

    content: str | None = ""

    source: str

    url: str

    published_at: str