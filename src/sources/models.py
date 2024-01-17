import os.path
import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.config import DEFAULT_ICON_NAME, global_settings


class Source(Base):
    __tablename__ = "source"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False, unique=True)
    url = Column(String(256), nullable=False, unique=True)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("user_folder.id"), nullable=False)
    folder = relationship("UserFolder", back_populates="sources")
    icon = Column(
        String(256), nullable=False, server_default=os.path.join(global_settings.icons_path, DEFAULT_ICON_NAME)
    )
