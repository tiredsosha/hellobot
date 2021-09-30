from pydantic import BaseModel


class Bot(BaseModel):
    singing: str = '5672df6abcdcdfbbdcbdfea0ab52135e'
    token: str = 'xoxb-1572232124883-2138932977143-kSVbvCD3zzFFDdA1CUMpaT25'
    endpoint: str = '/slack/events'