import secrets
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.table import TableModel
from app.repositories.restaurant_repository import (
    RestaurantRepository,
)
from app.repositories.table_repository import TableRepository
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    """
    Contains business logic related to restaurant tables.
    """

    def __init__(
        self,
        repository: TableRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.repository = repository
        self.restaurant_repository = restaurant_repository

    def create_table(
        self,
        data: TableCreate,
    ) -> dict:
        """
        Create a new table.
        """

        # Verify that the restaurant exists.
        restaurant = self.restaurant_repository.get_by_id(
            data.restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Restaurant "
                    f"{data.restaurant_id} not found"
                ),
            )

        # Check whether the restaurant already has
        # this table number.
        existing_table = (
            self.repository.get_by_restaurant_and_number(
                data.restaurant_id,
                data.table_number,
            )
        )

        if existing_table:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Table {data.table_number} "
                    f"already exists in restaurant "
                    f"{data.restaurant_id}"
                ),
            )

        # Get all existing tables.
        existing_tables = self.repository.get_all(
            data.restaurant_id
        )

        # Generate the next table ID.
        table_number_for_id = len(existing_tables) + 1

        table_id = (
            f"TABLE{table_number_for_id:03d}"
        )

        # Generate a secure random token.
        #
        # This will eventually be represented
        # in the table's QR code.
        qr_token = secrets.token_urlsafe(16)

        # Create MongoDB document.
        table = TableModel.create_document(
            table_id=table_id,
            restaurant_id=data.restaurant_id,
            table_number=data.table_number,
            capacity=data.capacity,
            status=data.status,
            qr_token=qr_token,
        )

        # Save to MongoDB.
        return self.repository.create(table)

    def get_all_tables(
        self,
        restaurant_id: str | None = None,
    ) -> list[dict]:
        """
        Return tables.

        Optionally filter by restaurant_id.
        """

        return self.repository.get_all(
            restaurant_id
        )

    def get_table(
        self,
        table_id: str,
    ) -> dict:
        """
        Return one table.
        """

        table = self.repository.get_by_id(
            table_id
        )

        if table is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table {table_id} not found",
            )

        return table

    def update_table(
        self,
        table_id: str,
        data: TableUpdate,
    ) -> dict:
        """
        Update a table.
        """

        # Make sure table exists.
        existing_table = self.get_table(table_id)

        # Get only fields supplied by the client.
        update_data = data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        # If table number is being changed,
        # check for duplicates.
        if "table_number" in update_data:

            duplicate = (
                self.repository
                .get_by_restaurant_and_number(
                    existing_table["restaurant_id"],
                    update_data["table_number"],
                )
            )

            # Make sure the duplicate isn't the
            # same table we're currently updating.
            if (
                duplicate
                and duplicate["table_id"] != table_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Table "
                        f"{update_data['table_number']} "
                        f"already exists in this restaurant"
                    ),
                )

        # Update timestamp.
        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        return self.repository.update(
            table_id,
            update_data,
        )

    def delete_table(
        self,
        table_id: str,
    ) -> None:
        """
        Delete a table.
        """

        # Make sure table exists.
        self.get_table(table_id)

        deleted = self.repository.delete(
            table_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table {table_id} not found",
            )
