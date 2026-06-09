from __future__ import annotations

from backend.app.main import health


def test_health():
    assert health()["status"] == "ok"

