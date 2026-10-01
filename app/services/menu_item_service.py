from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status

from app.models.menu_item import MenuItemModel
from app.repositories.category_repository import (
    CategoryRepository,
)
from app.repositories.menu_item_repository import (
    MenuItemRepository,
)
from app.repositories.restaurant_repository import (
    RestaurantRepository,
)
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
)


class MenuItemService:
    """
    Business logic for restaurant menu items.
    """

    def __init__(
        self,
        repository: MenuItemRepository,
        restaurant_repository: RestaurantRepository,
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.restaurant_repository = (
            restaurant_repository
        )
        self.category_repository = (
            category_repository
        )

    def create_item(
        self,
        data: MenuItemCreate,
    ) -> dict:
        """
        Create a menu item.
        """

        # Verify restaurant.
        restaurant = (
            self.restaurant_repository.get_by_id(
                data.restaurant_id
            )
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Restaurant "
                    f"{data.restaurant_id} not found"
                ),
            )

        # Verify category.
        category = (
            self.category_repository.get_by_id(
                data.category_id
            )
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Category "
                    f"{data.category_id} not found"
                ),
            )

        # Make sure category belongs to restaurant.
        if (
            category["restaurant_id"]
            != data.restaurant_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Category does not belong "
                    "to this restaurant"
                ),
            )

        # Prevent duplicate item names.
        existing = self.repository.get_by_name(
            data.restaurant_id,
            data.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Menu item '{data.name}' "
                    f"already exists"
                ),
            )

        # Generate ID.
        existing_items = self.repository.get_all(
            data.restaurant_id
        )

        item_number = len(existing_items) + 1

        item_id = f"ITEM{item_number:03d}"

        # Create document.
        item = MenuItemModel.create_document(
            item_id=item_id,
            restaurant_id=data.restaurant_id,
            category_id=data.category_id,
            name=data.name,
            description=data.description,
            price=data.price,
        )

        return self.repository.create(item)

    def get_all_items(
        self,
        restaurant_id: str | None = None,
        category_id: str | None = None,
    ) -> list[dict]:
        """
        Get menu items with optional filters.
        """

        return self.repository.get_all(
            restaurant_id,
            category_id,
        )

    def get_item(
        self,
        item_id: str,
    ) -> dict:
        """
        Get one menu item.
        """

        item = self.repository.get_by_id(
            item_id
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Menu item "
                    f"{item_id} not found"
                ),
            )

        return item

    def update_item(
        self,
        item_id: str,
        data: MenuItemUpdate,
    ) -> dict:
        """
        Update a menu item.
        """

        existing_item = self.get_item(item_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        # If category changes, verify new category.
        if "category_id" in update_data:

            category = (
                self.category_repository.get_by_id(
                    update_data["category_id"]
                )
            )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Category "
                        f"{update_data['category_id']} "
                        f"not found"
                    ),
                )

            if (
                category["restaurant_id"]
                != existing_item["restaurant_id"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Category does not belong "
                        "to this restaurant"
                    ),
                )

        # Convert Decimal price to string.
        if "price" in update_data:
            update_data["price"] = str(
                update_data["price"]
            )

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        return self.repository.update(
            item_id,
            update_data,
        )

    def delete_item(
        self,
        item_id: str,
    ) -> None:
        """
        Delete a menu item.
        """

        self.get_item(item_id)

        deleted = self.repository.delete(
            item_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Menu item "
                    f"{item_id} not found"
                ),
            )
