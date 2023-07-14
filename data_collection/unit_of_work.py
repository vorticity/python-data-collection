from abc import ABC, abstractmethod

from sqlmodel import create_engine, Session, SQLModel

from config import settings
from data_collection import models  # noqa: F401
from data_collection.repos import (
    SqlModelUsersRepo,
    TableConfigsRepo,
    TableViewsRepo,
    RowsRepo,
    UsersRepo,
    SqlModelRowsRepo,
    SqlModelTableConfigsRepo,
    SqlModelTableViewsRepo,
)  # noqa: E133


class UnitOfWork(ABC):
    rows: RowsRepo
    table_configs: TableConfigsRepo
    table_views: TableViewsRepo
    users: UsersRepo

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlModelUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        sqlite_url = f"sqlite:///{settings.db_path}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def __enter__(self):
        self.session = Session(self.engine)
        self.rows = SqlModelRowsRepo(self.session)
        self.table_configs = SqlModelTableConfigsRepo(self.session)
        self.table_views = SqlModelTableViewsRepo(self.session)
        self.users = SqlModelUsersRepo(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
