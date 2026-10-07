from typing import Literal
from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    request: str = Field(min_length=3, max_length=4000)
    application_id: str | None = None


class Plan(BaseModel):
    objective: str
    application_id: str
    environment: Literal["browser", "desktop"] = "browser"
    inputs: list[str] = []
    actions: list[str] = []
    expected_result: str
    risk_level: Literal["low", "medium", "high"] = "low"
    approval_may_be_required: bool = False


class Target(BaseModel):
    role: str | None = None
    name: str | None = None
    label: str | None = None
    text: str | None = None
    test_id: str | None = None


class Action(BaseModel):
    type: Literal["click", "fill", "press", "navigate", "download", "wait"]
    target: Target | None = None
    value: str | None = None
    risk: Literal["low", "medium", "high"] = "low"
    approval_required: bool = False


class ConnectorDefinition(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    name: str = Field(min_length=2, max_length=160)
    application_id: str
    environment: Literal["browser", "desktop"]
    inputs: list[str] = []
    preconditions: list[str] = []
    steps: list[Action] = Field(min_length=1)
    expected_result: str


class ApprovalRequest(BaseModel):
    approved: bool
