from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.restaurant import RestaurantModel
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
	"""
	Contains business logic related to restaurants.
	"""

	def __init__(self, repository: RestaurantRepository):
		self.repository = repository

	def create_restaurant(
		self,
		data: RestaurantCreate,
	) -> dict:
		"""
		Create a new restaurant.
		"""

		# Generate a simple readable restaurant ID.
		existing_restaurants = self.repository.get_all()

		restaurant_number = len(existing_restaurants) + 1

		restaurant_id = f"REST{restaurant_number:03d}"

		# Check whether this generated ID already exists.
		if self.repository.get_by_id(restaurant_id):
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail="Restaurant ID already exists",
			)

		# Convert Pydantic data into a normal dictionary.
		restaurant_data = data.model_dump()

		# Create MongoDB document.
		restaurant = RestaurantModel.create_document(
			restaurant_id=restaurant_id,
			name=restaurant_data["name"],
			description=restaurant_data.get("description"),
			address=restaurant_data["address"],
			phone=restaurant_data["phone"],
			status=restaurant_data["status"],
		)

		# Save restaurant.
		return self.repository.create(restaurant)

	def get_all_restaurants(self) -> list[dict]:
		"""
		Return all restaurants.
		"""

		return self.repository.get_all()

	def get_restaurant(
		self,
		restaurant_id: str,
	) -> dict:
		"""
		Return one restaurant.
		"""

		restaurant = self.repository.get_by_id(
			restaurant_id
		)

		if restaurant is None:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Restaurant {restaurant_id} not found",
			)

		return restaurant

	def update_restaurant(
		self,
		restaurant_id: str,
		data: RestaurantUpdate,
	) -> dict:
		"""
		Update an existing restaurant.
		"""

		# First verify the restaurant exists.
		self.get_restaurant(restaurant_id)

		# Only include fields actually supplied
		# by the client.
		update_data = data.model_dump(
			exclude_unset=True
		)

		if not update_data:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="No fields provided for update",
			)

		# Update timestamp.
		update_data["updated_at"] = datetime.now(
			timezone.utc
		)

		updated_restaurant = self.repository.update(
			restaurant_id,
			update_data,
		)

		return updated_restaurant

	def delete_restaurant(
		self,
		restaurant_id: str,
	) -> None:
		"""
		Delete an existing restaurant.
		"""

		# Verify that it exists first.
		self.get_restaurant(restaurant_id)

		deleted = self.repository.delete(
			restaurant_id
		)

		if not deleted:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Restaurant {restaurant_id} not found",
			)
