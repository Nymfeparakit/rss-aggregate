import uuid

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Source(Base):
    __tablename__ = "source"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False)
    url = Column(String(256), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("source_folder.id"), nullable=False)


class SourcesFolder(Base):
    __tablename__ = "source_folder"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False)
    sources = relationship("Source", backref="folder")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"folder {self.id}, name - {self.name}"
