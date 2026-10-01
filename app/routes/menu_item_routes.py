from fastapi import APIRouter, Depends, status

from app.database.mongodb import database
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
    MenuItemResponse,
    MenuItemUpdate,
)
from app.services.menu_item_service import (
    MenuItemService,
)


router = APIRouter(
    prefix="/api/menu-items",
    tags=["Menu Items"],
)


def get_menu_item_service() -> MenuItemService:
    """
    Build MenuItemService dependencies.
    """

    item_collection = database[
        "menu_items"
    ]

    category_collection = database[
        "categories"
    ]

    restaurant_collection = database[
        "restaurants"
    ]

    item_repository = MenuItemRepository(
        item_collection
    )

    category_repository = CategoryRepository(
        category_collection
    )

    restaurant_repository = RestaurantRepository(
        restaurant_collection
    )

    return MenuItemService(
        repository=item_repository,
        restaurant_repository=restaurant_repository,
        category_repository=category_repository,
    )


@router.post(
    "",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(
    data: MenuItemCreate,
    service: MenuItemService = Depends(
        get_menu_item_service
    ),
):
    """
    Create a menu item.
    """

    return service.create_item(data)


@router.get(
    "",
    response_model=list[MenuItemResponse],
)
def get_menu_items(
    restaurant_id: str | None = None,
    category_id: str | None = None,
    service: MenuItemService = Depends(
        get_menu_item_service
    ),
):
    """
    Get menu items.

    Examples:

    /api/menu-items?restaurant_id=REST001

    /api/menu-items?
        restaurant_id=REST001&
        category_id=CAT001
    """

    return service.get_all_items(
        restaurant_id,
        category_id,
    )


@router.get(
    "/{item_id}",
    response_model=MenuItemResponse,
)
def get_menu_item(
    item_id: str,
    service: MenuItemService = Depends(
        get_menu_item_service
    ),
):
    """
    Get one menu item.
    """

    return service.get_item(item_id)


@router.put(
    "/{item_id}",
    response_model=MenuItemResponse,
)
def update_menu_item(
    item_id: str,
    data: MenuItemUpdate,
    service: MenuItemService = Depends(
        get_menu_item_service
    ),
):
    """
    Update menu item.
    """

    return service.update_item(
        item_id,
        data,
    )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_menu_item(
    item_id: str,
    service: MenuItemService = Depends(
        get_menu_item_service
    ),
):
    """
    Delete menu item.
    """

    service.delete_item(item_id)

    return None
