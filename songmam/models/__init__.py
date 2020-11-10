from pydantic import BaseModel


class ThingWithId(BaseModel):
    id: str

    @property
    def isNone(self):
        return self.id == "none"

    @classmethod
    def create_none(cls):
        return cls(id="none")
