from fastapi import APIRouter

from app.database.mongodb import check_database_connection


# APIRouter allows us to keep related endpoints
# in a separate file.
router = APIRouter(
	prefix="/api/health",
	tags=["Health"],
)


@router.get("")
def health_check():
	"""
	Basic application health check.

	This endpoint tells us whether
	the FastAPI application is running.
	"""

	return {
		"status": "healthy",
		"service": "restaurant-qr-ordering-api",
	}


@router.get("/db")
def database_health_check():
	"""
	Database health check.

	This endpoint verifies whether
	FastAPI can communicate with MongoDB.
	"""

	is_connected = check_database_connection()

	if is_connected:
		return {
			"status": "healthy",
			"database": "connected",
		}

	return {
		"status": "unhealthy",
		"database": "disconnected",
	}
