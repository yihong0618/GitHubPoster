import datetime
import sys
import types

import pytest

from github_poster.loader.strava_loader import StravaLoader


class FakeFault(Exception):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


class FakeClient:
    pass


@pytest.fixture
def fake_stravalib(monkeypatch):
    module = types.ModuleType("stravalib")
    module.Client = FakeClient
    module.exc = types.SimpleNamespace(Fault=FakeFault)
    monkeypatch.setitem(sys.modules, "stravalib", module)
    return module


def make_loader(fake_stravalib):
    return StravaLoader(
        2024,
        2024,
        "strava",
        strava_client_id="client-id",
        strava_client_secret="client-secret",
        strava_refresh_token="refresh-token",
    )


def make_fault(status_code):
    response = types.SimpleNamespace(status_code=status_code)
    return FakeFault(f"{status_code} Server Error", response=response)


def test_strava_loader_retries_server_fault(monkeypatch, fake_stravalib):
    loader = make_loader(fake_stravalib)
    activity = types.SimpleNamespace(
        distance=1234,
        start_date_local=datetime.datetime(2024, 1, 2, 3, 4, 5),
    )
    calls = {"count": 0}
    sleeps = []

    def get_api_data():
        calls["count"] += 1
        if calls["count"] == 1:
            raise make_fault(597)
        return [activity]

    monkeypatch.setattr(loader, "get_api_data", get_api_data)
    monkeypatch.setattr("github_poster.loader.strava_loader.time.sleep", sleeps.append)

    assert loader.make_track_dict() == [activity]
    assert calls["count"] == 2
    assert sleeps == [5]
    assert loader.number_by_date_dict["2024-01-02"] == 1.23


def test_strava_loader_does_not_retry_client_fault(monkeypatch, fake_stravalib):
    loader = make_loader(fake_stravalib)
    calls = {"count": 0}

    def get_api_data():
        calls["count"] += 1
        raise make_fault(401)

    monkeypatch.setattr(loader, "get_api_data", get_api_data)

    with pytest.raises(FakeFault):
        loader.make_track_dict()

    assert calls["count"] == 1
