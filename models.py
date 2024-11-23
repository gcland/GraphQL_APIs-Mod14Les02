from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Inventory(Base):
    __tablename__ = "Inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
    quantity: Mapped[int] = mapped_column(db.Integer)
    price: Mapped[float] = mapped_column(db.Float)
    category: Mapped[str] = mapped_column(db.String(255))