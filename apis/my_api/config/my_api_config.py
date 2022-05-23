from pydantic import BaseSettings


class MyApiSettings(BaseSettings):
    PORT: int
    HOST: str


def get_myapi_settings() -> MyApiSettings:
    return MyApiSettings()
