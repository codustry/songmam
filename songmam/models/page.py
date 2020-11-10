from pydantic import BaseModel


class Page(BaseModel):
    id: str
    name: str
