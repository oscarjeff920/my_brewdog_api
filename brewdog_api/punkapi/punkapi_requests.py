import fastapi
import pydantic.error_wrappers
import requests  # type: ignore
import typing as _typing

from brewdog_api.punkapi.config.punkapi_config import PunkApiSettings
from lib.schemas.beer_schemas import FullBeerBase
from lib.schemas.pydantic_schemas import Malt, Amount, Hops


def get_json_data_obj(path: str) -> _typing.Dict:
    try:
        response = requests.get(path)  # type: ignore
        response.raise_for_status()
    except requests.exceptions.HTTPError:  # type: ignore
        if 400 <= response.status_code < 500:
            raise fastapi.HTTPException(status_code=404, detail="Could not find beers")
        else:
            raise fastapi.HTTPException(status_code=500, detail="Error Api Server side")
    # Add other error catches
    try:
        details = response.json()
    except requests.exceptions.JSONDecodeError:  # type: ignore
        raise fastapi.HTTPException(status_code=406, detail="Response not JSONable")
    return details


def create_beer_obj(json_response: _typing.Dict) -> FullBeerBase:
    try:
        used_malts = []
        for malt in json_response["ingredients"]["malt"]:
            used_malts.append(
                Malt(
                    name=malt["name"],
                    amount=Amount(
                        value=malt["amount"]["value"], unit=malt["amount"]["unit"]
                    ),
                )
            )
        used_hops = []
        for hops in json_response["ingredients"]["hops"]:
            used_hops.append(
                Hops(
                    name=hops["name"],
                    amount=Amount(
                        value=hops["amount"]["value"], unit=hops["amount"]["unit"]
                    ),
                    add=hops["add"],
                    attribute=hops["attribute"],
                )
            )
        listed_beer = FullBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            first_brewed=json_response["first_brewed"],
            description=json_response["description"],
            image_url=json_response["image_url"],
            abv=json_response["abv"],
            ingredients=dict(
                malt=used_malts,
                hops=used_hops,
                yeast=json_response["ingredients"]["yeast"],
            ),
            colour_rating=dict(ebc=json_response["ebc"], srm=json_response["srm"]),
            ibu=json_response["ibu"],
            ph=json_response["ph"],
        )
        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )


# The already defined api calls from the punkapi api
def get_all_beers(api_settings: PunkApiSettings) -> _typing.List[FullBeerBase]:
    path = api_settings.PUNKAPI_URL

    details = get_json_data_obj(path=path)

    list_of_beers = []

    for beer in details:
        listed_beer = create_beer_obj(json_response=beer)

        list_of_beers.append(listed_beer)

    return list_of_beers


def get_beer_by_id(api_settings: PunkApiSettings, beer_id: int) -> FullBeerBase:
    path = "{}/{}".format(api_settings.PUNKAPI_URL, beer_id)

    details = get_json_data_obj(path=path)

    listed_beer = create_beer_obj(json_response=details[0])
    return listed_beer


def get_random_beer(api_settings: PunkApiSettings) -> FullBeerBase:
    path = "{}/random".format(api_settings.PUNKAPI_URL)

    details = get_json_data_obj(path=path)

    listed_beer = create_beer_obj(json_response=details[0])
    return listed_beer


# My Api calls
def get_beer_by_name(api_settings: PunkApiSettings, beer_name: str) -> FullBeerBase:
    beer_name = beer_name.lower()

    all_beers = get_all_beers(api_settings=api_settings)

    queried_beer = None
    for beer in all_beers:
        if beer.name.lower() == beer_name:
            return beer

    if not queried_beer:
        raise fastapi.HTTPException(
            status_code=404, detail="Beer : {} not found".format(beer_name)
        )


def get_beer_with_lower_abv(
    api_settings: PunkApiSettings, abv: float
) -> _typing.List[FullBeerBase]:
    all_beers = get_all_beers(api_settings=api_settings)

    queried_beers = []
    for beer in all_beers:
        if beer.abv <= abv:
            queried_beers.append(beer)

    if not queried_beers:
        fastapi.HTTPException(
            status_code=404, detail="No beers found with abv <= {}".format(abv)
        )
    return queried_beers


def get_beer_with_higher_abv(
    api_settings: PunkApiSettings, abv: float
) -> _typing.List[FullBeerBase]:
    all_beers = get_all_beers(api_settings=api_settings)

    queried_beers = []
    for beer in all_beers:
        if beer.abv >= abv:
            queried_beers.append(beer)

    if not queried_beers:
        fastapi.HTTPException(
            status_code=404, detail="No beers found with abv >= {}".format(abv)
        )
    return queried_beers


def get_beers_with_hops(
    api_settings: PunkApiSettings, queried_hops: str
) -> _typing.List[FullBeerBase]:
    queried_hops = queried_hops.lower()
    all_beers = get_all_beers(api_settings=api_settings)

    queried_beers = []
    for beer in all_beers:
        added = False
        for hops in beer.ingredients.hops:
            if hops.name.lower() == queried_hops:
                added = True
                break
        if added:
            queried_beers.append(beer)

    if not queried_beers:
        fastapi.HTTPException(
            status_code=404, detail="No beers found with hop {}".format(queried_hops)
        )
    return queried_beers


def get_beers_with_malt(
    api_settings: PunkApiSettings, queried_malt: str
) -> _typing.List[FullBeerBase]:
    queried_malt = queried_malt.lower()
    all_beers = get_all_beers(api_settings=api_settings)

    queried_beers = []
    for beer in all_beers:
        added = False
        for malt in beer.ingredients.malt:
            if malt.name.lower() == queried_malt:
                added = True
                break
        if added:
            queried_beers.append(beer)

    if not queried_beers:
        fastapi.HTTPException(
            status_code=404, detail="No beers found with malt {}".format(queried_malt)
        )
    return queried_beers
