from pydantic import BaseModel as _BaseModel
import typing as _typing
from lib.schemas.sub_nested_schemas import Ingredients as _Ingredients, Malt, Hops
from lib.schemas.sub_nested_schemas import ColourScale as _ColourScale


class BeerBase(_BaseModel):
    id: int
    name: str
    tagline: str
    image_url: _typing.Optional[str] = None


class FullBeerBase(BeerBase):
    first_brewed: str
    description: str
    abv: float
    ingredients: _Ingredients
    colour_rating: _ColourScale
    ibu: _typing.Optional[int] = None
    ph: _typing.Optional[float] = None


class AllBeerBase(BeerBase):
    description: str
    abv: float


class AbvBeerBase(BeerBase):
    abv: float


class MaltBeerBase(BeerBase):
    malt: _typing.List[Malt]


class HopsBeerBase(BeerBase):
    hops: _typing.List[Hops]


class YeastBeerBase(BeerBase):
    yeast: str
