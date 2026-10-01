from datetime import datetime, timezone


class CategoryModel:
    """
    Creates MongoDB documents for menu categories.
    """

    @staticmethod
    def create_document(
        category_id: str,
        restaurant_id: str,
        name: str,
        description: str | None,
    ) -> dict:
        """
        Build the MongoDB category document.
        """

        now = datetime.now(timezone.utc)

        return {
            "category_id": category_id,
            "restaurant_id": restaurant_id,
            "name": name,
            "description": description,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
