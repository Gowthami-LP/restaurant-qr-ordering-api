from fastapi import APIRouter, Depends, status

from app.database.mongodb import database
from app.repositories.restaurant_repository import (
	RestaurantRepository,
)
from app.schemas.restaurant import (
	RestaurantCreate,
	RestaurantResponse,
	RestaurantUpdate,
)
from app.services.restaurant_service import (
	RestaurantService,
)


router = APIRouter(
	prefix="/api/restaurants",
	tags=["Restaurants"],
)


def get_restaurant_service() -> RestaurantService:
	"""
	Dependency function.

	Creates the repository and service required
	by our restaurant endpoints.
	"""

	collection = database["restaurants"]

	repository = RestaurantRepository(collection)

	return RestaurantService(repository)


@router.post(
	"",
	response_model=RestaurantResponse,
	status_code=status.HTTP_201_CREATED,
)
def create_restaurant(
	data: RestaurantCreate,
	service: RestaurantService = Depends(
		get_restaurant_service
	),
):
	"""
	Create a new restaurant.
	"""

	return service.create_restaurant(data)


@router.get(
	"",
	response_model=list[RestaurantResponse],
)
def get_restaurants(
	service: RestaurantService = Depends(
		get_restaurant_service
	),
):
	"""
	Get all restaurants.
	"""

	return service.get_all_restaurants()


@router.get(
	"/{restaurant_id}",
	response_model=RestaurantResponse,
)
def get_restaurant(
	restaurant_id: str,
	service: RestaurantService = Depends(
		get_restaurant_service
	),
):
	"""
	Get one restaurant using restaurant_id.
	"""

	return service.get_restaurant(restaurant_id)


@router.put(
	"/{restaurant_id}",
	response_model=RestaurantResponse,
)
def update_restaurant(
	restaurant_id: str,
	data: RestaurantUpdate,
	service: RestaurantService = Depends(
		get_restaurant_service
	),
):
	"""
	Update a restaurant.
	"""

	return service.update_restaurant(
		restaurant_id,
		data,
	)


@router.delete(
	"/{restaurant_id}",
	status_code=status.HTTP_204_NO_CONTENT,
)
def delete_restaurant(
	restaurant_id: str,
	service: RestaurantService = Depends(
		get_restaurant_service
	),
):
	"""
	Delete a restaurant.
	"""

	service.delete_restaurant(restaurant_id)

	# 204 responses should not contain a response body.
	return None
