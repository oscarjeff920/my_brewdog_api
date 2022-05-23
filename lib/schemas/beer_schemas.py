from pydantic import BaseModel as _BaseModel
import typing as _typing
from lib.schemas.pydantic_schemas import Ingredients as _Ingredients
from lib.schemas.pydantic_schemas import ColourScale as _ColourScale


class FullBeerBase(_BaseModel):
    id: int
    name: str
    tagline: str
    first_brewed: str
    description: str
    image_url: str
    abv: float
    ingredients: _Ingredients
    colour_rating: _ColourScale
    ibu: _typing.Optional[int] = None
    ph: _typing.Optional[float] = None
