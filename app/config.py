from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str = 'localhost'
    db_port: Optional[int]
    db_user: str = 'admin'
    db_pass: str = 'test'
    db_name: str = 'test'
    redis_url: str = 'localhost'

    @property
    def db_url(self):
        if self.db_port:
            return f'{self.db_host}:{self.db_port}'
        else:
            return self.db_host


settings = Settings()
