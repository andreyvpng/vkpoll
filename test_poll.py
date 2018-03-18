import pytest

from vkpoll import app


@pytest.fixture
def application():
    app.config.update({
        'TESTING': True
    })
    return app


@pytest.fixture
def client(application):
    return app.test_client()


def test_index():
    assert 2 + 2 == 4
