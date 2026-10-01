from typing import Literal

from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    """
    Request schema used when creating a restaurant table.
    """

    # Restaurant to which this table belongs.
    restaurant_id: str = Field(
        ...,
        min_length=3,
        description="ID of the restaurant",
    )

    # Physical table number inside the restaurant.
    table_number: int = Field(
        ...,
        gt=0,
        description="Physical table number",
    )

    # Maximum number of people who can sit at the table.
    capacity: int = Field(
        ...,
        gt=0,
        le=20,
        description="Maximum seating capacity",
    )

    # New tables are available by default.
    status: Literal[
        "available",
        "occupied",
        "reserved",
        "inactive",
    ] = "available"


class TableUpdate(BaseModel):
    """
    Request schema used when updating a table.

    Fields are optional because we may update only
    one or two properties.
    """

    table_number: int | None = Field(
        default=None,
        gt=0,
    )

    capacity: int | None = Field(
        default=None,
        gt=0,
        le=20,
    )

    status: Literal[
        "available",
        "occupied",
        "reserved",
        "inactive",
    ] | None = None


class TableResponse(BaseModel):
    """
    Response schema returned by the API.
    """

    table_id: str
    restaurant_id: str
    table_number: int
    capacity: int

    status: Literal[
        "available",
        "occupied",
        "reserved",
        "inactive",
    ]

    qr_token: str
