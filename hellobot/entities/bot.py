from pydantic import BaseModel


class Bot(BaseModel):
    singing: str = 'xxxxx'
    token: str = 'xoxb-xxxx'
    endpoint: str = '/slack/events'