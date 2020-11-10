import pytest
from decouple import config
from faker import Faker
from songmam import MessengerApi
from songmam.models.webhook.events.messages import Sender


@pytest.fixture
def api():
    """
    Return an api token.

    Args:
    """
    return MessengerApi(access_token=config("access_token"))


@pytest.fixture
def faker():
    """
    Returns a faker

    Args:
    """
    return Faker()


@pytest.fixture
def recipient():
    """
    Recipientate a recipient.

    Args:
    """
    return


@pytest.fixture
def test_user():
    """
    Return a user sender.

    Args:
    """
    # Tan
    return Sender(id="2945944152161824")
