import typing as _typing
from pydantic import BaseModel as _BaseModel


class ColourScale(_BaseModel):
    ebc: _typing.Optional[int] = None
    srm: _typing.Optional[int] = None


class Amount(_BaseModel):
    value: float
    unit: str


class Malt(_BaseModel):
    name: str
    amount: Amount


class Hops(Malt):
    add: str
    attribute: str


class Ingredients(_BaseModel):
    malt: _typing.List[Malt]
    hops: _typing.List[Hops]
    yeast: str
