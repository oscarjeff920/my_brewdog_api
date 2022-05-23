from pydantic import BaseSettings


class PunkApiSettings(BaseSettings):
    API_URL: str


def get_punkapi_settings() -> PunkApiSettings:
    return PunkApiSettings()
