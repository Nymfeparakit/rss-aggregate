import uuid

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.sources.models import Source


class FolderHasSourceAssociation(Base):
    __tablename__ = "folder_has_source"
    folder_id = Column(ForeignKey("source_folder.id"), primary_key=True)
    source_id = Column(ForeignKey("source.id"), primary_key=True)
    folder = relationship("UserFolder", back_populates="sources")
    source = relationship(Source, back_populates="folders")


class UserFolder(Base):
    __tablename__ = "source_folder"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    sources = relationship("FolderHasSourceAssociation", back_populates="folder")

    def __repr__(self) -> str:
        return f"folder {self.id}, name - {self.name}"
