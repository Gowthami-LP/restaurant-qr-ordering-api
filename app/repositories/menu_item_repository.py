from pymongo.collection import Collection


class MenuItemRepository:
    """
    Handles MongoDB operations for menu items.
    """

    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, item: dict) -> dict:
        """
        Insert menu item.
        """

        self.collection.insert_one(item)

        return item

    def get_all(
        self,
        restaurant_id: str | None = None,
        category_id: str | None = None,
    ) -> list[dict]:
        """
        Get menu items.

        Supports filtering by restaurant and category.
        """

        query = {}

        if restaurant_id:
            query["restaurant_id"] = restaurant_id

        if category_id:
            query["category_id"] = category_id

        return list(
            self.collection.find(
                query,
                {"_id": 0},
            )
        )

    def get_by_id(
        self,
        item_id: str,
    ) -> dict | None:
        """
        Get one menu item.
        """

        return self.collection.find_one(
            {"item_id": item_id},
            {"_id": 0},
        )

    def get_by_name(
        self,
        restaurant_id: str,
        name: str,
    ) -> dict | None:
        """
        Find an item by name inside a restaurant.
        """

        return self.collection.find_one(
            {
                "restaurant_id": restaurant_id,
                "name": name,
            },
            {"_id": 0},
        )

    def update(
        self,
        item_id: str,
        update_data: dict,
    ) -> dict | None:
        """
        Update a menu item.
        """

        self.collection.update_one(
            {"item_id": item_id},
            {"$set": update_data},
        )

        return self.get_by_id(item_id)

    def delete(
        self,
        item_id: str,
    ) -> bool:
        """
        Delete a menu item.
        """

        result = self.collection.delete_one(
            {"item_id": item_id}
        )

        return result.deleted_count > 0
