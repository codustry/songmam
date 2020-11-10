import pytest
from faker import Faker
from songmam.api.content import ContentButton
from songmam.models.messaging.payload import CompletePayload
from songmam.models.persona import Persona


@pytest.fixture
def page():
    return Page()


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def recipient():
    return


@pytest.mark.asyncio
async def test_main_line(page):
    aPersona = Persona(
        name="Nina Trinity",
        profile_picture_url="https://vignette.wikia.nocookie.net/gundam/images/4/49/Gundam00_16-2.jpg/revision/latest?cb=20200126233658",
    )
    res = await page.create_persona(aPersona)
    # content = CompletePayload(
    #     recipient=
    # )
    # page.send_native()
