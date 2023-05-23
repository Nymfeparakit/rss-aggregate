import uuid

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Source(Base):
    __tablename__ = "source"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False, unique=True)
    url = Column(String(256), nullable=False, unique=True)
    folders = relationship("FolderHasSourceAssociation", back_populates="source")
