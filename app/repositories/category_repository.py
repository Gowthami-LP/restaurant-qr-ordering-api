from pymongo.collection import Collection


class CategoryRepository:
    """
    Handles MongoDB operations for categories.
    """

    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, category: dict) -> dict:
        """
        Insert a category into MongoDB.
        """

        self.collection.insert_one(category)

        return category

    def get_all(
        self,
        restaurant_id: str | None = None,
    ) -> list[dict]:
        """
        Get all categories.

        If restaurant_id is supplied,
        return categories for that restaurant only.
        """

        query = {}

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
        category_id: str,
    ) -> dict | None:
        """
        Find one category by category_id.
        """

        return self.collection.find_one(
            {"category_id": category_id},
            {"_id": 0},
        )

    def get_by_name(
        self,
        restaurant_id: str,
        name: str,
    ) -> dict | None:
        """
        Find a category by name within a restaurant.
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
        category_id: str,
        update_data: dict,
    ) -> dict | None:
        """
        Update a category.
        """

        self.collection.update_one(
            {"category_id": category_id},
            {"$set": update_data},
        )

        return self.get_by_id(category_id)

    def delete(
        self,
        category_id: str,
    ) -> bool:
        """
        Delete a category.
        """

        result = self.collection.delete_one(
            {"category_id": category_id}
        )

        return result.deleted_count > 0
