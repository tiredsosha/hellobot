from pydantic import BaseModel, validator


class Email(BaseModel):
    username: str
    password: str
