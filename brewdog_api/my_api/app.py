from fastapi import FastAPI
import typing as _typing

from brewdog_api.punkapi.config.punkapi_config import get_punkapi_settings
from brewdog_api.punkapi.requests import my_requests, punkapi_requests
from lib.schemas.beer_schemas import (
    AllBeerBase,
    FullBeerBase,
    AbvBeerBase,
    MaltBeerBase,
    HopsBeerBase,
    YeastBeerBase,
)

app = FastAPI()


@app.get("/", tags=["Index"])
async def index() -> _typing.Dict:
    return {"Home": "An Api to receive data from the brewdog punkapi database"}


# Punkapi endpoints
@app.get("/beers", response_model=_typing.List[AllBeerBase], tags=["Punkapi Api Calls"])
async def get_all_beers() -> _typing.List[AllBeerBase]:
    return punkapi_requests.get_all_beers(api_settings=get_punkapi_settings())


@app.get("/beers/random", response_model=FullBeerBase, tags=["Punkapi Api Calls"])
async def get_random_beer() -> FullBeerBase:
    return punkapi_requests.get_random_beer(api_settings=get_punkapi_settings())


@app.get("/beers/id/{beer_id}", response_model=FullBeerBase, tags=["Punkapi Api Calls"])
async def get_beer_by_id(beer_id: int) -> FullBeerBase:
    return punkapi_requests.get_beer_by_id(
        api_settings=get_punkapi_settings(), beer_id=beer_id
    )


# My Api endpoints
@app.get(
    "/beers/name/{beer_name}", response_model=FullBeerBase, tags=["Extra Api Calls"]
)
async def get_beer_by_name(beer_name: str) -> FullBeerBase:
    return my_requests.get_beer_by_name(
        api_settings=get_punkapi_settings(), beer_name=beer_name
    )


@app.get(
    "/beers/abv/less/{abv_value}",
    response_model=_typing.List[AbvBeerBase],
    tags=["Extra Api Calls", "ABV"],
)
async def get_beers_with_lower_abv(abv_value: float) -> _typing.List[AbvBeerBase]:
    return my_requests.get_beers_with_lower_abv(
        api_settings=get_punkapi_settings(), abv=abv_value
    )


@app.get(
    "/beers/abv/more/{abv_value}",
    response_model=_typing.List[AbvBeerBase],
    tags=["Extra Api Calls", "ABV"],
)
async def get_beers_with_higher_abv(abv_value: float) -> _typing.List[AbvBeerBase]:
    return my_requests.get_beers_with_higher_abv(
        api_settings=get_punkapi_settings(), abv=abv_value
    )


@app.get(
    "/beers/ingredients/malt/{malt_name}",
    response_model=_typing.List[MaltBeerBase],
    tags=["Extra Api Calls", "Ingredients"],
)
async def get_beers_with_malt(malt_name: str) -> _typing.List[MaltBeerBase]:
    return my_requests.get_beers_with_malt(
        api_settings=get_punkapi_settings(), queried_malt=malt_name
    )


@app.get(
    "/beers/ingredients/hops/{hops_name}",
    response_model=_typing.List[HopsBeerBase],
    tags=["Extra Api Calls", "Ingredients"],
)
async def get_beers_with_hops(hops_name: str) -> _typing.List[HopsBeerBase]:
    return my_requests.get_beers_with_hops(
        api_settings=get_punkapi_settings(), queried_hops=hops_name
    )


@app.get(
    "/beers/ingredients/yeast/{yeast_name}",
    response_model=_typing.List[YeastBeerBase],
    tags=["Extra Api Calls", "Ingredients"],
)
async def get_beers_with_yeast(yeast_name: str) -> _typing.List[YeastBeerBase]:
    return my_requests.get_beers_with_yeast(
        api_settings=get_punkapi_settings(), queried_yeast=yeast_name
    )
