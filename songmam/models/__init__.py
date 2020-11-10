from pydantic import BaseModel


class ThingWithId(BaseModel):
    id: str

    @property
    def isNone(self):
        """
        Return true if the id is the id of the database.

        Args:
            self: (todo): write your description
        """
        return self.id == "none"

    @classmethod
    def create_none(cls):
        """
        Create a new : class.

        Args:
            cls: (callable): write your description
        """
        return cls(id="none")
