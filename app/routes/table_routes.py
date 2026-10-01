from fastapi import APIRouter, Depends, status

from app.database.mongodb import database
from app.repositories.restaurant_repository import (
    RestaurantRepository,
)
from app.repositories.table_repository import (
    TableRepository,
)
from app.schemas.table import (
    TableCreate,
    TableResponse,
    TableUpdate,
)
from app.services.table_service import TableService


router = APIRouter(
    prefix="/api/tables",
    tags=["Tables"],
)


def get_table_service() -> TableService:
    """
    Build the dependencies required by TableService.
    """

    # MongoDB collections.
    table_collection = database["tables"]

    restaurant_collection = database[
        "restaurants"
    ]

    # Create repositories.
    table_repository = TableRepository(
        table_collection
    )

    restaurant_repository = RestaurantRepository(
        restaurant_collection
    )

    # Create service.
    return TableService(
        repository=table_repository,
        restaurant_repository=restaurant_repository,
    )


@router.post(
    "",
    response_model=TableResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_table(
    data: TableCreate,
    service: TableService = Depends(
        get_table_service
    ),
):
    """
    Create a new restaurant table.
    """

    return service.create_table(data)


@router.get(
    "",
    response_model=list[TableResponse],
)
def get_tables(
    restaurant_id: str | None = None,
    service: TableService = Depends(
        get_table_service
    ),
):
    """
    Get all tables.

    Optional query parameter:

    ?restaurant_id=REST001
    """

    return service.get_all_tables(
        restaurant_id
    )


@router.get(
    "/{table_id}",
    response_model=TableResponse,
)
def get_table(
    table_id: str,
    service: TableService = Depends(
        get_table_service
    ),
):
    """
    Get one table by table_id.
    """

    return service.get_table(table_id)


@router.put(
    "/{table_id}",
    response_model=TableResponse,
)
def update_table(
    table_id: str,
    data: TableUpdate,
    service: TableService = Depends(
        get_table_service
    ),
):
    """
    Update a table.
    """

    return service.update_table(
        table_id,
        data,
    )


@router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_table(
    table_id: str,
    service: TableService = Depends(
        get_table_service
    ),
):
    """
    Delete a table.
    """

    service.delete_table(table_id)

    return None
