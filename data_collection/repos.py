from typing import Protocol

from sqlmodel import select, Session

from data_collection.models import TableConfig, TableView, Row, User
from data_collection.exceptions import EntityNotFound


class TableConfigsRepo(Protocol):
    def add(self, entity: TableConfig) -> TableConfig:
        ...

    def delete(self, id: int) -> None:
        ...

    def get_by_id(self, id: int) -> TableConfig:
        ...

    def find_by_name(self, name: str) -> TableConfig:
        ...

    def all(self) -> list[TableConfig]:
        ...


class TableViewsRepo(Protocol):
    def add(self, entity: TableView) -> TableView:
        ...

    def delete(self, id: int) -> None:
        ...

    def get_by_id(self, id: int) -> TableView:
        ...

    def find_by_name(self, name: str) -> TableView:
        ...

    def all(self) -> list[TableView]:
        ...


class RowsRepo(Protocol):
    def add(self, entity: Row) -> Row:
        ...

    def delete(self, id: int) -> None:
        ...

    def get_by_id(self, id: int) -> Row:
        ...

    def all(self) -> list[Row]:
        ...


class UsersRepo(Protocol):
    def add(self, entity: User) -> User:
        ...

    def delete(self, id: int) -> None:
        ...

    def get_by_id(self, id: int) -> User:
        ...

    def all(self) -> list[User]:
        ...


class SqlModelTableConfigsRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, table_config: TableConfig) -> TableConfig:
        self.session.add(table_config)
        self.session.commit()
        self.session.refresh(table_config)
        self.session.expunge_all()
        return table_config

    def delete(self, table_config_id: int) -> None:
        self.session.delete(self.get_by_id(table_config_id))

    def get_by_id(self, table_config_id: int) -> TableConfig:
        user = self.session.get(TableConfig, table_config_id)
        self.session.expunge_all()
        if not user:
            raise EntityNotFound("table_config_id not found")
        return user

    def all(self) -> list[TableConfig]:
        statement = select(TableConfig)
        results = self.session.execute(statement)
        results = list(i[0] for i in results.all())
        self.session.expunge_all()
        if len(results) == 0:
            return []
        return results


class SqlModelTableViewsRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, table_view: TableView) -> TableView:
        self.session.add(table_view)
        self.session.commit()
        self.session.refresh(table_view)
        self.session.expunge_all()
        return table_view

    def delete(self, table_view_id: int) -> None:
        self.session.delete(self.get_by_id(table_view_id))

    def get_by_id(self, table_view_id: int) -> TableView:
        user = self.session.get(TableView, table_view_id)
        self.session.expunge_all()
        if not user:
            raise EntityNotFound("table_view_id not found")
        return user

    def all(self) -> list[TableView]:
        statement = select(TableView)
        results = self.session.execute(statement)
        results = list(i[0] for i in results.all())
        self.session.expunge_all()
        if len(results) == 0:
            return []
        return results


class SqlModelRowsRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, row: Row) -> Row:
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        self.session.expunge_all()
        return row

    def delete(self, row_id: int) -> None:
        self.session.delete(self.get_by_id(row_id))

    def get_by_id(self, row_id: int) -> Row:
        row = self.session.get(Row, row_id)
        self.session.expunge_all()
        if not row:
            raise EntityNotFound("row_id not found")
        return row

    def all(self) -> list[Row]:
        statement = select(Row)
        results = self.session.execute(statement)
        results = list(i[0] for i in results.all())
        self.session.expunge_all()
        if len(results) == 0:
            return []
        return results


class SqlModelUsersRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.session.expunge_all()
        return user

    def delete(self, user_id: int) -> None:
        self.session.delete(self.get_by_id(user_id))

    def get_by_id(self, user_id: int) -> User:
        user = self.session.get(User, user_id)
        self.session.expunge_all()
        if not user:
            raise EntityNotFound("user_id not found")
        return user

    def all(self) -> list[User]:
        statement = select(User)
        results = self.session.execute(statement)
        results = list(i[0] for i in results.all())
        self.session.expunge_all()
        if len(results) == 0:
            return []
        return results
