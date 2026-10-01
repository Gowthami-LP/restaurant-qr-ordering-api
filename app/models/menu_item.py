from datetime import datetime, timezone
from decimal import Decimal


class MenuItemModel:
    """
    Creates MongoDB documents for menu items.
    """

    @staticmethod
    def create_document(
        item_id: str,
        restaurant_id: str,
        category_id: str,
        name: str,
        description: str | None,
        price: Decimal,
    ) -> dict:
        """
        Build a MongoDB menu item document.
        """

        now = datetime.now(timezone.utc)

        return {
            "item_id": item_id,
            "restaurant_id": restaurant_id,
            "category_id": category_id,
            "name": name,
            "description": description,

            # Convert Decimal to string for predictable
            # JSON/MongoDB handling in this learning project.
            "price": str(price),

            "is_available": True,

            "created_at": now,
            "updated_at": now,
        }
