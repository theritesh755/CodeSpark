from sqlalchemy import String, Integer, DateTime, JSON, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from database.postgres import Base

class TraceRecord(Base):
    __tablename__ = "trace_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trace_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    subject: Mapped[str] = mapped_column(String(128), index=True)
    chain: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(24), default="completed")
    result_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
