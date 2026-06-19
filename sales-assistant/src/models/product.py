from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.lead import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    purchase_url: Mapped[str | None] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
