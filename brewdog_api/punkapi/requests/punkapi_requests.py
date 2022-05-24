from brewdog_api.punkapi.config.punkapi_config import PunkApiSettings
import typing as _typing

from brewdog_api.punkapi.requests.get_data import (
    get_json_data_obj,
    create_full_beer_base_obj,
    create_all_beer_base_obj,
)

from lib.schemas.beer_schemas import FullBeerBase, AllBeerBase


def get_all_beers(api_settings: PunkApiSettings) -> _typing.List[AllBeerBase]:
    path = api_settings.PUNKAPI_URL

    details = get_json_data_obj(path=path)

    list_of_beers = []

    for beer in details:
        listed_beer = create_all_beer_base_obj(json_response=beer)

        list_of_beers.append(listed_beer)

    return list_of_beers


def get_beer_by_id(api_settings: PunkApiSettings, beer_id: int) -> FullBeerBase:
    path = "{}/{}".format(api_settings.PUNKAPI_URL, beer_id)

    details = get_json_data_obj(path=path)

    listed_beer = create_full_beer_base_obj(json_response=details[0])
    return listed_beer


def get_random_beer(api_settings: PunkApiSettings) -> FullBeerBase:
    path = "{}/random".format(api_settings.PUNKAPI_URL)

    details = get_json_data_obj(path=path)

    listed_beer = create_full_beer_base_obj(json_response=details[0])
    return listed_beer
