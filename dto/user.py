from pydantic import BaseModel
"""Data Transfer Object"""
class User(BaseModel):
    name: str