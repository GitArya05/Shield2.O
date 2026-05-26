from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Shield Navigation API"
    VERSION: str = "v1"
    # Pydantic will automatically look for this in your .env file
    DATABASE_URL: str 

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize the settings to be imported across the app
settings = Settings()