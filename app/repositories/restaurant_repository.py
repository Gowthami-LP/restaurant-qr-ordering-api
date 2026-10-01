from typing import Any

from pymongo.collection import Collection


class RestaurantRepository:
	"""
	Handles all MongoDB operations related to restaurants.

	The service layer will call this repository instead
	of directly communicating with MongoDB.
	"""

	def __init__(self, collection: Collection):
		"""
		Receive the MongoDB restaurants collection.
		"""

		self.collection = collection

	def create(self, restaurant: dict) -> dict:
		"""
		Insert a restaurant document into MongoDB.
		"""

		self.collection.insert_one(restaurant)

		return restaurant

	def get_all(self) -> list[dict]:
		"""
		Return all restaurants.
		"""

		return list(
			self.collection.find(
				{},
				{"_id": 0},
			)
		)

	def get_by_id(self, restaurant_id: str) -> dict | None:
		"""
		Find one restaurant using restaurant_id.
		"""

		return self.collection.find_one(
			{"restaurant_id": restaurant_id},
			{"_id": 0},
		)

	def update(
		self,
		restaurant_id: str,
		update_data: dict,
	) -> dict | None:
		"""
		Update an existing restaurant.
		"""

		self.collection.update_one(
			{"restaurant_id": restaurant_id},
			{"$set": update_data},
		)

		return self.get_by_id(restaurant_id)

	def delete(self, restaurant_id: str) -> bool:
		"""
		Delete a restaurant.

		Returns:
			True if a document was deleted.
			False if no restaurant was found.
		"""

		result = self.collection.delete_one(
			{"restaurant_id": restaurant_id}
		)

		return result.deleted_count > 0
