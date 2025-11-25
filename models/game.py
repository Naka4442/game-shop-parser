from pydantic import BaseModel


class Game(BaseModel):
    title: str
    price: int
    url: str

    discount: float | None = None
    image_url: str | None = None
