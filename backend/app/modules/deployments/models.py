from app.database.models_base import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[UUID] = mapped_column
