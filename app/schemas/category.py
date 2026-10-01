from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """
    Request schema used when creating a category.
    """

    # Restaurant that owns this category.
    restaurant_id: str = Field(
        ...,
        min_length=3,
        description="ID of the restaurant",
    )

    # Category name such as Starters or Desserts.
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name",
    )

    # Optional explanation of the category.
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Category description",
    )


class CategoryUpdate(BaseModel):
    """
    Request schema used when updating a category.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    is_active: bool | None = None


class CategoryResponse(BaseModel):
    """
    Response returned by the category APIs.
    """

    category_id: str
    restaurant_id: str
    name: str
    description: str | None
    is_active: bool
