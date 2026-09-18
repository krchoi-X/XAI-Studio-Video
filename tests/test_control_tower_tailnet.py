"""The Open Gallery link has to survive Control Tower starting before Tailscale does."""
from __future__ import annotations

import control_tower.monitor as monitor_module
from control_tower.config import Config
from control_tower.monitor import MonitorService
from control_tower.tailscale import parse_serve_status

SERVE_STATUS = """https://artxorn.tailf10079.ts.net (tailnet only)
|-- / proxy http://127.0.0.1:8787

https://artxorn.tailf10079.ts.net:8443 (tailnet only)
|-- / proxy http://127.0.0.1:8800

https://artxorn.tailf10079.ts.net:8790 (tailnet only)
|-- / proxy http://127.0.0.1:8790
"""


def test_serve_status_maps_each_local_port_to_its_own_origin() -> None:
    assert parse_serve_status(SERVE_STATUS, 8787) == "https://artxorn.tailf10079.ts.net/"
    assert parse_serve_status(SERVE_STATUS, 8800) == "https://artxorn.tailf10079.ts.net:8443/"
    assert parse_serve_status(SERVE_STATUS, 8790) == "https://artxorn.tailf10079.ts.net:8790/"
    assert parse_serve_status(SERVE_STATUS, 9999) is None


def _service(tmp_path, answers: list[str | None]) -> tuple[MonitorService, list[int]]:
    calls: list[int] = []

    def fake_detect(port: int, *_args, **_kwargs) -> str | None:
        calls.append(port)
        return answers[min(len(calls) - 1, len(answers) - 1)]

    monitor_module.detect_served_url = fake_detect
    config = Config()
    config.database_path = tmp_path / "ct.db"
    return MonitorService(config), calls


def test_a_probe_that_found_nothing_at_startup_is_tried_again(tmp_path) -> None:
    service, calls = _service(tmp_path, [None, "https://artxorn.tailf10079.ts.net/"])
    try:
        assert service.gallery_tailnet_url is None
        assert service._sample_gallery_tailnet_url() is False
        assert service.gallery_tailnet_url is None

        assert service._sample_gallery_tailnet_url() is True
        assert service.gallery_tailnet_url == "https://artxorn.tailf10079.ts.net/"
        assert calls == [config_port(service), config_port(service)]
    finally:
        service.db.close()


def test_a_failed_probe_never_clears_a_link_that_works(tmp_path) -> None:
    service, _ = _service(tmp_path, ["https://artxorn.tailf10079.ts.net/", None])
    try:
        service._sample_gallery_tailnet_url()
        assert service.gallery_tailnet_url == "https://artxorn.tailf10079.ts.net/"
        assert service._sample_gallery_tailnet_url() is False
        assert service.gallery_tailnet_url == "https://artxorn.tailf10079.ts.net/"
    finally:
        service.db.close()


def test_an_explicit_setting_pins_the_url_and_stops_the_probing(tmp_path) -> None:
    calls: list[int] = []

    def fake_detect(port: int, *_args, **_kwargs) -> str | None:
        calls.append(port)
        return "https://detected.example/"

    monitor_module.detect_served_url = fake_detect
    config = Config()
    config.database_path = tmp_path / "ct.db"
    config.gallery_tailnet_url = "https://pinned.example/"
    service = MonitorService(config)
    try:
        assert service.gallery_tailnet_url == "https://pinned.example/"
        assert service._sample_gallery_tailnet_url() is False
        assert service.gallery_tailnet_url == "https://pinned.example/"
        assert calls == []
    finally:
        service.db.close()


def config_port(service: MonitorService) -> int:
    return service.config.gallery_port
