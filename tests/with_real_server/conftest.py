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
    # Ben, Saku Jobbot
    return Sender(id=config('test_user_psid'))
