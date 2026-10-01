from decimal import Decimal

from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    """
    Request schema for creating a menu item.
    """

    restaurant_id: str = Field(
        ...,
        min_length=3,
    )

    category_id: str = Field(
        ...,
        min_length=3,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    # Decimal is better than float for money.
    price: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
    )


class MenuItemUpdate(BaseModel):
    """
    Request schema for updating a menu item.
    """

    category_id: str | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    price: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
    )

    is_available: bool | None = None


class MenuItemResponse(BaseModel):
    """
    Response returned by menu item APIs.
    """

    item_id: str
    restaurant_id: str
    category_id: str
    name: str
    description: str | None
    price: Decimal
    is_available: bool
