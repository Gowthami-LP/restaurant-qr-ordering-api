from datetime import datetime, timezone


class RestaurantModel:
	"""
	Represents the structure of a restaurant document
	that will be stored in MongoDB.

	This is a simple application model rather than
	a MongoDB ODM model.
	"""

	@staticmethod
	def create_document(
		restaurant_id: str,
		name: str,
		description: str | None,
		address: str,
		phone: str,
		status: str,
	) -> dict:
		"""
		Build a MongoDB document for a restaurant.
		"""

		now = datetime.now(timezone.utc)

		return {
			"restaurant_id": restaurant_id,
			"name": name,
			"description": description,
			"address": address,
			"phone": phone,
			"status": status,
			"created_at": now,
			"updated_at": now,
		}
