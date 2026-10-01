from fastapi import FastAPI

from app.config.settings import settings
from app.routes.category_routes import (
	router as category_router,
)
from app.routes.health_routes import router as health_router
from app.routes.restaurant_routes import (
	router as restaurant_router,
)
from app.routes.table_routes import (
	router as table_router,
)
from app.routes.menu_item_routes import (
	router as menu_item_router,
)


# Create the FastAPI application.
app = FastAPI(
	title=settings.app_name,
	description="Backend API for QR-based restaurant ordering",
	version="1.0.0",
)


# Health APIs
app.include_router(health_router)

# Restaurant APIs
app.include_router(restaurant_router)

# Table APIs
app.include_router(table_router)

# Category APIs
app.include_router(category_router)

# Menu item APIs
app.include_router(menu_item_router)


@app.get("/")
def root():
	"""
	Root endpoint.

	Used to verify that the API application
	itself is running.
	"""

	return {
		"message": "Restaurant QR Ordering API is running"
	}
