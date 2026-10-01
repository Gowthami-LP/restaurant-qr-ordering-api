from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.category import CategoryModel
from app.repositories.category_repository import (
    CategoryRepository,
)
from app.repositories.restaurant_repository import (
    RestaurantRepository,
)
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:
    """
    Contains business logic for menu categories.
    """

    def __init__(
        self,
        repository: CategoryRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.repository = repository
        self.restaurant_repository = restaurant_repository

    def create_category(
        self,
        data: CategoryCreate,
    ) -> dict:
        """
        Create a new category.
        """

        # Verify restaurant exists.
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

        # Prevent duplicate category names.
        existing = self.repository.get_by_name(
            data.restaurant_id,
            data.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Category '{data.name}' "
                    f"already exists"
                ),
            )

        # Generate category ID.
        existing_categories = self.repository.get_all(
            data.restaurant_id
        )

        category_number = len(
            existing_categories
        ) + 1

        category_id = (
            f"CAT{category_number:03d}"
        )

        # Create MongoDB document.
        category = CategoryModel.create_document(
            category_id=category_id,
            restaurant_id=data.restaurant_id,
            name=data.name,
            description=data.description,
        )

        return self.repository.create(category)

    def get_all_categories(
        self,
        restaurant_id: str | None = None,
    ) -> list[dict]:
        """
        Get all categories.
        """

        return self.repository.get_all(
            restaurant_id
        )

    def get_category(
        self,
        category_id: str,
    ) -> dict:
        """
        Get one category.
        """

        category = self.repository.get_by_id(
            category_id
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Category "
                    f"{category_id} not found"
                ),
            )

        return category

    def update_category(
        self,
        category_id: str,
        data: CategoryUpdate,
    ) -> dict:
        """
        Update a category.
        """

        # Verify category exists.
        self.get_category(category_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        return self.repository.update(
            category_id,
            update_data,
        )

    def delete_category(
        self,
        category_id: str,
    ) -> None:
        """
        Delete a category.
        """

        self.get_category(category_id)

        deleted = self.repository.delete(
            category_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Category "
                    f"{category_id} not found"
                ),
            )
