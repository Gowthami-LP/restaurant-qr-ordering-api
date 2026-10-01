from typing import Literal

from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
	"""
	Schema used when creating a new restaurant.

	This defines what data the client is allowed
	to send to the create-restaurant API.
	"""

	name: str = Field(
		...,
		min_length=2,
		max_length=100,
		description="Restaurant name",
	)

	description: str | None = Field(
		default=None,
		max_length=500,
		description="Short description of the restaurant",
	)

	address: str = Field(
		...,
		min_length=5,
		max_length=250,
		description="Restaurant address",
	)

	phone: str = Field(
		...,
		min_length=10,
		max_length=15,
		description="Restaurant contact number",
	)

	status: Literal["active", "inactive"] = "active"


class RestaurantUpdate(BaseModel):
	"""
	Schema used when updating an existing restaurant.

	All fields are optional because PATCH/PUT can
	update only the information that is provided.
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

	address: str | None = Field(
		default=None,
		min_length=5,
		max_length=250,
	)

	phone: str | None = Field(
		default=None,
		min_length=10,
		max_length=15,
	)

	status: Literal["active", "inactive"] | None = None


class RestaurantResponse(BaseModel):
	"""
	Schema returned to the client.

	This controls the format of our API response.
	"""

	restaurant_id: str
	name: str
	description: str | None = None
	address: str
	phone: str
	status: Literal["active", "inactive"]
