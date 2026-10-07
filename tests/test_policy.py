import pytest
from app.schemas import Action, ConnectorDefinition, Target
from app.services.policy import PolicyError, validate_connector


def connector(**kwargs):
    data = {"name":"Example connector", "application_id":"mock-fund-portal", "environment":"browser",
            "expected_result":"result is shown", "steps":[{"type":"click", "target":{"role":"button","name":"Search"}}]}
    data.update(kwargs)
    return ConnectorDefinition.model_validate(data)


def test_allowlisted_connector_passes():
    assert validate_connector(connector()).application_id == "mock-fund-portal"


def test_unregistered_application_is_rejected():
    with pytest.raises(PolicyError, match="not allowlisted"):
        validate_connector(connector(application_id="unknown-app"))


def test_navigation_outside_allowlist_is_rejected():
    with pytest.raises(PolicyError, match="domain"):
        validate_connector(connector(steps=[{"type":"navigate", "value":"https://evil.example", "risk":"low", "approval_required":False}]))
