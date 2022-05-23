from fastapi import FastAPI
import typing as _typing

from brewdog_api.punkapi import punkapi_requests
from brewdog_api.punkapi.config.punkapi_config import get_punkapi_settings
from lib.schemas.beer_schemas import FullBeerBase as _FullBeerBase

app = FastAPI()


@app.get("/")
async def index() -> _typing.Dict:
    return {"Home": "An Api to receive data from the brewdog punkapi database"}


@app.get("/beers/", response_model=_typing.List[_FullBeerBase])
async def get_all_beers() -> _typing.List[_FullBeerBase]:
    return punkapi_requests.get_all_beers(api_settings=get_punkapi_settings())
