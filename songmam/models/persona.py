from typing import List

from pydantic import BaseModel, HttpUrl


class Persona(BaseModel):
    name: str
    profile_picture_url: HttpUrl


class PersonaWithId(Persona):
    id: str


class PersonaResponse(BaseModel):
    id: str


class Cursors(BaseModel):
    before: str
    after: str


class Paging(BaseModel):
    cursors: Cursors


class AllPerosnasResponse(BaseModel):
    data: List[PersonaWithId]
    paging: Paging


class PersonaDeleteResponse(BaseModel):
    success: bool
