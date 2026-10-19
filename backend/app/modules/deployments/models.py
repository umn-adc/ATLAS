from app.database.models_base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[UUID] = mapped_column
