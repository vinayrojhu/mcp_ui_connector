from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Connector(Base):
    __tablename__ = "connectors"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(160))
    application_id: Mapped[str] = mapped_column(String(120), index=True)
    environment: Mapped[str] = mapped_column(String(20))
    version: Mapped[int] = mapped_column(Integer, default=1)
    definition: Mapped[dict] = mapped_column(JSON)
    fingerprint: Mapped[str] = mapped_column(String(128), default="")
    status: Mapped[str] = mapped_column(String(20), default="active")
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Execution(Base):
    __tablename__ = "executions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    connector_id: Mapped[str | None] = mapped_column(ForeignKey("connectors.id"), nullable=True)
    request: Mapped[str] = mapped_column(Text)
    definition: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="pending")
    events: Mapped[list] = mapped_column(JSON, default=list)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    execution_id: Mapped[str] = mapped_column(String(36), index=True)
    event_type: Mapped[str] = mapped_column(String(80))
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
