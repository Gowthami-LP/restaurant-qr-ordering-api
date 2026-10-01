from datetime import datetime, timezone


class TableModel:
    """
    Creates the MongoDB document structure for a table.
    """

    @staticmethod
    def create_document(
        table_id: str,
        restaurant_id: str,
        table_number: int,
        capacity: int,
        status: str,
        qr_token: str,
    ) -> dict:
        """
        Build a table document that can be stored in MongoDB.
        """

        # Use timezone-aware UTC timestamps.
        now = datetime.now(timezone.utc)

        return {
            "table_id": table_id,
            "restaurant_id": restaurant_id,
            "table_number": table_number,
            "capacity": capacity,
            "status": status,
            "qr_token": qr_token,
            "created_at": now,
            "updated_at": now,
        }
