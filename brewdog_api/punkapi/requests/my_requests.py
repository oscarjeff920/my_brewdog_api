import fastapi
import typing as _typing

from brewdog_api.punkapi.config.punkapi_config import PunkApiSettings
from brewdog_api.punkapi.requests.get_data import (
    get_json_data_obj,
    create_full_beer_base_obj,
)
from brewdog_api.punkapi.requests.get_data import (
    create_abv_beer_base_obj,
    create_malt_beer_base_obj,
)
from brewdog_api.punkapi.requests.get_data import (
    create_hops_beer_base_obj,
    create_yeast_beer_base_obj,
)

from lib.schemas.beer_schemas import (
    FullBeerBase,
    AbvBeerBase,
    MaltBeerBase,
    HopsBeerBase,
    YeastBeerBase,
)


def get_beer_by_name(api_settings: PunkApiSettings, beer_name: str) -> FullBeerBase:
    path = api_settings.PUNKAPI_URL
    beer_name = beer_name.lower()

    all_beers = get_json_data_obj(path=path)

    for beer in all_beers:
        if beer["name"].lower() == beer_name:
            return create_full_beer_base_obj(json_response=beer)
    else:
        raise fastapi.HTTPException(
            status_code=404, detail="Beer not found: {}".format(beer_name)
        )


def get_beers_with_lower_abv(
    api_settings: PunkApiSettings, abv: float
) -> _typing.List[AbvBeerBase]:
    URL = api_settings.PUNKAPI_URL

    all_beers = get_json_data_obj(path=URL)

    queried_beers = []
    for beer in all_beers:
        if beer["abv"] <= abv:
            queried_beers.append(create_abv_beer_base_obj(beer))

    if not queried_beers:
        raise fastapi.HTTPException(
            status_code=404, detail="No beers found with abv <= {}".format(abv)
        )
    return queried_beers


def get_beers_with_higher_abv(
    api_settings: PunkApiSettings, abv: float
) -> _typing.List[AbvBeerBase]:
    URL = api_settings.PUNKAPI_URL

    all_beers = get_json_data_obj(path=URL)

    queried_beers = []
    for beer in all_beers:
        if beer["abv"] >= abv:
            queried_beers.append(create_abv_beer_base_obj(beer))

    if not queried_beers:
        raise fastapi.HTTPException(
            status_code=404, detail="No beers found with abv <= {}".format(abv)
        )
    return queried_beers


def get_beers_with_hops(
    api_settings: PunkApiSettings, queried_hops: str
) -> _typing.List[HopsBeerBase]:
    URL = api_settings.PUNKAPI_URL
    queried_hops = queried_hops.lower()

    all_beers = get_json_data_obj(path=URL)

    queried_beers = []
    for beer in all_beers:
        added = False
        for hops in beer["ingredients"]["hops"]:
            if hops["name"].lower() == queried_hops:
                added = True
                break
        if added:
            queried_beers.append(create_hops_beer_base_obj(beer))

    if not queried_beers:
        raise fastapi.HTTPException(
            status_code=404, detail="No beers found with hop {}".format(queried_hops)
        )
    return queried_beers


def get_beers_with_malt(
    api_settings: PunkApiSettings, queried_malt: str
) -> _typing.List[MaltBeerBase]:
    URL = api_settings.PUNKAPI_URL
    queried_malt = queried_malt.lower()

    all_beers = get_json_data_obj(path=URL)

    queried_beers = []
    for beer in all_beers:
        added = False
        for malt in beer["ingredients"]["malt"]:
            if malt["name"].lower() == queried_malt:
                added = True
                break
        if added:
            queried_beers.append(create_malt_beer_base_obj(beer))

    if not queried_beers:
        raise fastapi.HTTPException(
            status_code=404, detail="No beers found with malt {}".format(queried_malt)
        )
    return queried_beers


def get_beers_with_yeast(
    api_settings: PunkApiSettings, queried_yeast: str
) -> _typing.List[YeastBeerBase]:
    URL = api_settings.PUNKAPI_URL
    queried_yeast = queried_yeast.lower()

    all_beers = get_json_data_obj(path=URL)

    queried_beers = []
    for beer in all_beers:
        # Not a very good solution, but data is inconsistent
        if beer["ingredients"]["yeast"].lower().find(queried_yeast) == 0:
            queried_beers.append(create_yeast_beer_base_obj(beer))

    if not queried_beers:
        raise fastapi.HTTPException(
            status_code=404, detail="No beers found with yeast {}".format(queried_yeast)
        )
    return queried_beers
