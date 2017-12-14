import pytest

from cenotes_lib import crypto


@pytest.fixture(scope="session", name="testing_key")
def _key():
    return crypto.craft_key_from_password("testing")


@pytest.fixture(scope="session", name="testing_box")
def _box(testing_key):
    return crypto.craft_secret_box(testing_key)
