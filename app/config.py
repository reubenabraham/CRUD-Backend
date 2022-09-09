from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        #This env file is searched from the root of the project folder it looks like, so no need for ../.env
        env_file = ".env"


settings = Settings()

