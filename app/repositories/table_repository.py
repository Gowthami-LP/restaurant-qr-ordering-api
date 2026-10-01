from pymongo.collection import Collection


class TableRepository:
    """
    Handles MongoDB operations for restaurant tables.
    """

    def __init__(self, collection: Collection):
        """
        Receive the MongoDB tables collection.
        """

        self.collection = collection

    def create(self, table: dict) -> dict:
        """
        Insert a table into MongoDB.
        """

        self.collection.insert_one(table)

        return table

    def get_all(
        self,
        restaurant_id: str | None = None,
    ) -> list[dict]:
        """
        Get all tables.

        If restaurant_id is provided, only tables
        belonging to that restaurant are returned.
        """

        # Start with an empty MongoDB filter.
        query = {}

        # Add restaurant filter when supplied.
        if restaurant_id:
            query["restaurant_id"] = restaurant_id

        return list(
            self.collection.find(
                query,
                {"_id": 0},
            )
        )

    def get_by_id(
        self,
        table_id: str,
    ) -> dict | None:
        """
        Find one table using table_id.
        """

        return self.collection.find_one(
            {"table_id": table_id},
            {"_id": 0},
        )

    def get_by_restaurant_and_number(
        self,
        restaurant_id: str,
        table_number: int,
    ) -> dict | None:
        """
        Find a table using restaurant_id and table_number.

        This helps prevent duplicate table numbers
        within the same restaurant.
        """

        return self.collection.find_one(
            {
                "restaurant_id": restaurant_id,
                "table_number": table_number,
            },
            {"_id": 0},
        )

    def update(
        self,
        table_id: str,
        update_data: dict,
    ) -> dict | None:
        """
        Update a table.
        """

        self.collection.update_one(
            {"table_id": table_id},
            {"$set": update_data},
        )

        return self.get_by_id(table_id)

    def delete(
        self,
        table_id: str,
    ) -> bool:
        """
        Delete a table.

        Returns True when a table was deleted.
        """

        result = self.collection.delete_one(
            {"table_id": table_id}
        )

        return result.deleted_count > 0
