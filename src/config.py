from datetime import date

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_PASS_TEST: str
    DB_USER_TEST: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    NAME_ADMIN: str
    SURNAME_ADMIN: str
    BIRTHDATE_ADMIN: date  # 2021-12-30
    EMAIL_ADMIN: str
    PASSWORD_ADMIN: str

    @property
    def async_database_url(self):
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @property
    def async_database_url_test(self):
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}'
                f'/{self.DB_NAME_TEST}')

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
