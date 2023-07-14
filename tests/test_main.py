from fastapi import status
from fastapi.testclient import TestClient
from data_collection.constants import TableConfigName, TableViewName

from main import app


# users


def create_user(client) -> dict:
    response = client.post("/users", json={"name": "foobar"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_users(client) -> dict:
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_user(client, user_id: int):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_user(client, user_id: int):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_users():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_users(client)
        assert len(response) == 0
        # create an entry
        response = create_user(client)
        user_id = response["id"]
        # get entry
        response = get_user(client, user_id)
        assert response["id"] == user_id
        # get all entries
        response = get_all_users(client)
        assert len(response) == 1
        assert response[0]["id"] == user_id
        assert response[0]["name"] == "foobar"
        response = delete_user(client, user_id=user_id)
        response = get_all_users(client)
        assert len(response) == 0


# table configs


def create_table_config(client) -> dict:
    data = {
        "name": TableConfigName.FARMING_PRACTICE_CONFIG,
        "config_fields": {
            "columns": {
                "year": {"type": "int"},
                "crop_type": {"type": "str"},
                "tillage_depth": {"type": "float"},
                "comments": {"type": "str"},
                "is_tilled": {"type": "bool"},
                "external_account_id": {"type": "str"},
            }
        },
    }
    response = client.post("/table-configs", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_table_configs(client) -> dict:
    response = client.get("/table-configs")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_table_config(client, table_config_id: int):
    response = client.get(f"/table-configs/{table_config_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_table_config(client, table_config_id: int):
    response = client.delete(f"/table-configs/{table_config_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_table_configs():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_table_configs(client)
        assert len(response) == 0
        # create an entry
        response = create_table_config(client)
        table_config_id = response["id"]
        # get entry
        response = get_table_config(client, table_config_id)
        assert response["id"] == table_config_id
        print(response)
        assert len(response["config_fields"]["columns"].keys()) == 6
        # get all entries
        response = get_all_table_configs(client)
        assert len(response) == 1
        assert response[0]["id"] == table_config_id
        assert response[0]["name"] == TableConfigName.FARMING_PRACTICE_CONFIG
        response = delete_table_config(client, table_config_id=table_config_id)
        response = get_all_table_configs(client)
        assert len(response) == 0


# table views


def create_table_view(client, table_config_id) -> dict:
    data = {
        "name": TableViewName.FARMING_PRACTICE_OFFERING_VIEW,
        "table_config_id": table_config_id,
        "view_fields": {
            "columns": {
                "year": {},
                "is_tilled": {},
                "external_account_id": {"validation_regex": ".*"},
                "tillage_depth": {"display_type": "FLOAT_SLIDER"},
            },
            "num_rows": 5,
            "column_order": ["year", "is_tilled", "external_account_id", "tillage_depth"],
        },
    }
    response = client.post("/table-views", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_table_views(client) -> dict:
    response = client.get("/table-views")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_table_view(client, table_view_id: int):
    response = client.get(f"/table-views/{table_view_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_table_view(client, table_view_id: int):
    response = client.delete(f"/table-views/{table_view_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_table_views():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_table_views(client)
        assert len(response) == 0
        # create a table config
        response = create_table_config(client)
        table_config_id = response["id"]
        # create an entry
        response = create_table_view(client, table_config_id)
        table_view_id = response["id"]
        # get entry
        response = get_table_view(client, table_view_id)
        assert response["id"] == table_view_id
        assert len(response["view_fields"]["columns"]) == 4
        assert response["view_fields"]["columns"]["external_account_id"]["validation_regex"] == ".*"
        assert response["view_fields"]["columns"]["tillage_depth"]["display_type"] == "FLOAT_SLIDER"
        assert response["view_fields"]["num_rows"] == 5
        # get all entries
        response = get_all_table_views(client)
        assert len(response) == 1
        assert response[0]["id"] == table_view_id
        assert response[0]["name"] == TableViewName.FARMING_PRACTICE_OFFERING_VIEW
        response = delete_table_view(client, table_view_id=table_view_id)
        response = get_all_table_views(client)
        assert len(response) == 0


# rows


def create_row(client, table_config_id) -> dict:
    data = {
        "table_config_id": table_config_id,
        "data": {
            "year": 2023,
            "crop_type": "BARLEY",
            "tillage_depth": 10,
            "comments": "Regrow Ag Challenge",
            "is_tilled": True,
            "external_account_id": "ABAFCE13123124",
        },
    }
    response = client.post("/rows", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_rows(client) -> dict:
    response = client.get("/rows")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_row(client, row_id: int):
    response = client.get(f"/rows/{row_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_row(client, row_id: int):
    response = client.delete(f"/rows/{row_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_rows():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_rows(client)
        assert len(response) == 0
        # create a table config
        response = create_table_config(client)
        table_config_id = response["id"]
        # create an entry
        response = create_row(client, table_config_id)
        row_id = response["id"]
        # get entry
        response = get_row(client, row_id)
        assert response["id"] == row_id
        assert response["data"]["year"] == 2023
        assert response["data"]["crop_type"] == "BARLEY"
        assert response["data"]["tillage_depth"] == 10
        assert response["data"]["comments"] == "Regrow Ag Challenge"
        assert response["data"]["is_tilled"] == True
        assert response["data"]["external_account_id"] == "ABAFCE13123124"
        # get all entries
        response = get_all_rows(client)
        assert len(response) == 1
        assert response[0]["id"] == row_id
        response = delete_row(client, row_id=row_id)
        response = get_all_rows(client)
        assert len(response) == 0
