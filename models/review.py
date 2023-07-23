#!/usr/bin/python3
""" holds class Review"""

import os
import sys
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Review(BaseModel, Base):
    """Representation of Review """
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
