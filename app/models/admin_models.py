import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, LargeBinary

from database import Base


class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key=True)
    admin_name = Column(String, nullable=False)
    admin_surname = Column(String, nullable=False)
    admin_email = Column(String, nullable=False)
    admin_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default='now()')
