from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Read environment variables with the same name
    it is case insensitive
    you can also default if none found"""
    model_config = SettingsConfigDict(env_file=".env")
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expiry_minutes: int

#    class ConfigDict:
#        env_file= ".env" # Sets variables from file

settings = Settings()