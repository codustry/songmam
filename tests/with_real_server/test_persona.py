import pytest
from pydantic import HttpUrl
from songmam.models.persona import Persona


@pytest.mark.asyncio
async def test_main_line(api):
      """
      Create a new apa.

      Args:
          api: (todo): write your description
      """
    aPersona = Persona(
        name="Nina Trinity",
        profile_picture_url=HttpUrl(
            "https://vignette.wikia.nocookie.net/gundam/images/4/49/Gundam00_16-2.jpg/revision/latest?cb=20200126233658"
        ),
    )
    res = await api.create_persona(aPersona)
    # content = CompletePayload(
    #     recipient=
    # )
    # page.send_native()
