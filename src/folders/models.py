import uuid

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class UserFolder(Base):
    __tablename__ = "user_folder"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    sources = relationship("Source", back_populates="folder")

    def __repr__(self) -> str:
        return f"folder {self.id}, name - {self.name}"
