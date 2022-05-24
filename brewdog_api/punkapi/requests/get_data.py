import typing as _typing

import fastapi
import pydantic
import requests as _requests

from lib.schemas.beer_schemas import (
    FullBeerBase,
    AllBeerBase,
    AbvBeerBase,
    MaltBeerBase,
    HopsBeerBase,
    YeastBeerBase,
)
from lib.schemas.sub_nested_schemas import Malt, Amount, Hops


def get_json_data_obj(path: str) -> _typing.Dict:
    try:
        response = _requests.get(path)  # type: ignore
        response.raise_for_status()
    except _requests.exceptions.HTTPError:  # type: ignore
        if 400 <= response.status_code < 500:
            raise fastapi.HTTPException(status_code=404, detail="Could not find beers")
        else:
            raise fastapi.HTTPException(status_code=500, detail="Error Api Server side")
    # Add other error catches
    try:
        details = response.json()
    except _requests.exceptions.JSONDecodeError:  # type: ignore
        print(details)
        raise fastapi.HTTPException(status_code=406, detail="Response not JSONable")
    return details


def create_full_beer_base_obj(json_response: _typing.Dict) -> FullBeerBase:
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


def create_all_beer_base_obj(json_response: _typing.Dict) -> AllBeerBase:
    try:
        listed_beer = AllBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            description=json_response["description"],
            image_url=json_response["image_url"],
            abv=json_response["abv"],
        )
        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )


def create_abv_beer_base_obj(json_response: _typing.Dict) -> AbvBeerBase:
    try:
        listed_beer = AbvBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            image_url=json_response["image_url"],
            abv=json_response["abv"],
        )
        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )


def create_malt_beer_base_obj(json_response: _typing.Dict) -> MaltBeerBase:
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

        listed_beer = MaltBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            image_url=json_response["image_url"],
            malt=used_malts,
        )

        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )


def create_hops_beer_base_obj(json_response: _typing.Dict) -> HopsBeerBase:
    try:
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
        listed_beer = HopsBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            image_url=json_response["image_url"],
            hops=used_hops,
        )

        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )


def create_yeast_beer_base_obj(json_response: _typing.Dict) -> YeastBeerBase:
    try:
        listed_beer = YeastBeerBase(
            id=json_response["id"],
            name=json_response["name"],
            tagline=json_response["tagline"],
            image_url=json_response["image_url"],
            yeast=json_response["ingredients"]["yeast"],
        )
        return listed_beer

    except pydantic.error_wrappers.ValidationError:
        print(json_response)
        raise fastapi.HTTPException(
            status_code=406, detail="Received Json does not have required keys"
        )
