from fastapi import FastAPI, HTTPException, status

from data_collection.exceptions import EntityNotFound
from data_collection.models import User, Row, TableConfig, TableView
from data_collection.unit_of_work import SqlModelUnitOfWork

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global uow
    uow = SqlModelUnitOfWork()


# User


@app.get("/users", response_model=list[User])
async def get_users():
    with uow as context:
        return context.users.all()


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    with uow as context:
        try:
            return context.users.get_by_id(user_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="user_id not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    with uow as context:
        try:
            context.users.delete(user_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="user_id not found")
        finally:
            context.commit()
    return


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    with uow as context:
        return context.users.add(user)


# TableConfig


@app.get("/table-configs", response_model=list[TableConfig])
async def get_table_configs():
    with uow as context:
        return context.table_configs.all()


@app.get("/table-configs/{table_config_id}", response_model=TableConfig)
async def get_table_config(table_config_id: int):
    with uow as context:
        try:
            return context.table_configs.get_by_id(table_config_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="table_config_id not found")


@app.delete("/table-configs/{table_config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_config(table_config_id: int):
    with uow as context:
        try:
            context.table_configs.delete(table_config_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="table_config_id not found")
        finally:
            context.commit()
    return


@app.post(
    "/table-configs",
    status_code=status.HTTP_201_CREATED,
    response_model=TableConfig
    )
async def create_table_config(table_config: TableConfig):
    with uow as context:
        return context.table_configs.add(table_config)


# TableView


@app.get("/table-views", response_model=list[TableView])
async def get_table_views():
    with uow as context:
        return context.table_views.all()


@app.get("/table-views/{table_view_id}", response_model=TableView)
async def get_table_view(table_view_id: int):
    with uow as context:
        try:
            return context.table_views.get_by_id(table_view_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="table_view_id not found")


@app.delete("/table-views/{table_view_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_view(table_view_id: int):
    with uow as context:
        try:
            context.table_views.delete(table_view_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="table_view_id not found")
        finally:
            context.commit()
    return


@app.post("/table-views", status_code=status.HTTP_201_CREATED, response_model=TableView)
async def create_table_view(table_view: TableView):
    with uow as context:
        return context.table_views.add(table_view)


# Row


@app.get("/rows", response_model=list[Row])
async def get_rows():
    with uow as context:
        return context.rows.all()


@app.get("/rows/{row_id}", response_model=Row)
async def get_row(row_id: int):
    with uow as context:
        try:
            return context.rows.get_by_id(row_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="row_id not found")


@app.delete("/rows/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_row(row_id: int):
    with uow as context:
        try:
            context.rows.delete(row_id)
        except EntityNotFound:
            raise HTTPException(status_code=404, detail="row_id not found")
        finally:
            context.commit()
    return


@app.post("/rows", status_code=status.HTTP_201_CREATED, response_model=Row)
async def create_row(row: Row):
    with uow as context:
        return context.rows.add(row)
