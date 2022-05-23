import uvicorn

from brewdog_api.my_api.app import app
from brewdog_api.my_api.config.my_api_config import get_myapi_settings

if __name__ == "__main__":
    api_settings = get_myapi_settings()
    uvicorn.run(app, host=api_settings.API_HOST, port=api_settings.API_PORT)
