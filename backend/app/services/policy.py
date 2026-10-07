from app.core.config import get_settings
from app.schemas import ConnectorDefinition


class PolicyError(ValueError):
    pass


def validate_connector(connector: ConnectorDefinition) -> ConnectorDefinition:
    cfg = get_settings()
    if len(connector.steps) > cfg.max_connector_steps:
        raise PolicyError("Connector exceeds the configured step limit")
    allowed_apps = {v.strip() for v in cfg.allowed_applications.split(",") if v.strip()}
    if connector.application_id not in allowed_apps:
        raise PolicyError("Application is not allowlisted")
    for step in connector.steps:
        if step.type == "navigate":
            url = step.value or ""
            domain = url.split("/")[2].split(":")[0] if "://" in url else ""
            allowed_domains = {v.strip() for v in cfg.allowed_domains.split(",")}
            if domain not in allowed_domains:
                raise PolicyError("Navigation domain is not allowlisted")
        if step.type in {"fill", "click", "press", "download"} and step.target is None:
            raise PolicyError("UI action requires a target")
    return connector


def requires_approval(action) -> bool:
    return action.approval_required or action.risk == "high"
