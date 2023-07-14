from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, JSON, SQLModel

from data_collection.constants import TableConfigName, TableViewName


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Row(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    table_config_id: int = Field(foreign_key="tableconfig.id")
    data: dict = Field(default={}, sa_column=Column(JSON))


class TableConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: TableConfigName = Field(unique=True)
    config_fields: dict = Field(default={}, sa_column=Column(JSON))


class TableView(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: TableViewName = Field(unique=True)
    table_config_id: int = Field(foreign_key="tableconfig.id")
    view_fields: dict = Field(default={}, sa_column=Column(JSON))
