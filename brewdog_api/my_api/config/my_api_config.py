from pydantic import BaseSettings


class MyApiSettings(BaseSettings):
    API_PORT: int
    API_HOST: str


def get_myapi_settings() -> MyApiSettings:
    return MyApiSettings()
