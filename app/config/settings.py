from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	"""
	Application configuration.

	Values are loaded from the .env file.
	"""

	# Name displayed by our application
	app_name: str = "Restaurant QR Ordering API"

	# Current environment
	app_env: str = "development"

	# MongoDB connection URL
	mongo_uri: str = "mongodb://localhost:27017"

	# MongoDB database name
	mongo_database: str = "restaurant_db"

	# Tell Pydantic Settings to read values from .env
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


# Create one settings object that can be imported
# throughout our application.
settings = Settings()
