from pydantic import BaseModel


class Cred(BaseModel):
    username: str
    password: str
    master: str


def from_dict(data: dict):
    creds = {}
    for k, v in data.items():
        creds[k] = Cred(**v)
    return creds
