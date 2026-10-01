from fastapi import APIRouter, Depends, status

from app.database.mongodb import database
from app.repositories.category_repository import (
    CategoryRepository,
)
from app.repositories.restaurant_repository import (
    RestaurantRepository,
)
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import (
    CategoryService,
)


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


def get_category_service() -> CategoryService:
    """
    Build the CategoryService with its dependencies.
    """

    category_collection = database[
        "categories"
    ]

    restaurant_collection = database[
        "restaurants"
    ]

    category_repository = CategoryRepository(
        category_collection
    )

    restaurant_repository = RestaurantRepository(
        restaurant_collection
    )

    return CategoryService(
        repository=category_repository,
        restaurant_repository=restaurant_repository,
    )


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    """
    Create a menu category.
    """

    return service.create_category(data)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    restaurant_id: str | None = None,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    """
    Get categories.

    Example:

    /api/categories?restaurant_id=REST001
    """

    return service.get_all_categories(
        restaurant_id
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: str,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    """
    Get one category.
    """

    return service.get_category(category_id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: str,
    data: CategoryUpdate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    """
    Update category.
    """

    return service.update_category(
        category_id,
        data,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: str,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    """
    Delete category.
    """

    service.delete_category(category_id)

    return None
