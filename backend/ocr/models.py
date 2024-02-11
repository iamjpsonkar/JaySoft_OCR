from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

Base = declarative_base()

DB_URI = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///OCR.db")

class Image(Base):
    __tablename__ = 'images'

    image_id = Column(String, primary_key=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    image_name = Column(String(20))
    image_type = Column(String(20))
    base64image = Column(String)
    ocr_json = Column(String)

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "uploaded_date": self.upload_time.isoformat(),
            "image_name": self.image_name,
            "image_type": self.image_type,
            "base64image": self.base64image,
            "ocr_json": self.ocr_json
        }

