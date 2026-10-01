from pymongo import MongoClient
from pymongo.database import Database

from app.config.settings import settings


# Create a MongoDB client.
#
# MongoClient manages the connection between
# our FastAPI application and MongoDB.
client = MongoClient(settings.mongo_uri)


# Select our application database.
#
# If "restaurant_db" does not exist yet,
# MongoDB will create it when we store data.
database: Database = client[settings.mongo_database]


def check_database_connection() -> bool:
	"""
	Check whether MongoDB is reachable.

	Returns:
		True  -> MongoDB is reachable.
		False -> MongoDB connection failed.
	"""

	try:
		# ping sends a simple command to MongoDB.
		client.admin.command("ping")

		return True

	except Exception:
		# If MongoDB is unavailable, return False.
		return False
