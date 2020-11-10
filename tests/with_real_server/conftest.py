import pytest
from decouple import config
from faker import Faker
from songmam import MessengerApi
from songmam.models.webhook.events.messages import Sender


@pytest.fixture
def api():
    return MessengerApi(access_token=config("access_token"))


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def recipient():
    return


@pytest.fixture
def test_user():
    # Tan
    return Sender(id="2945944152161824")
