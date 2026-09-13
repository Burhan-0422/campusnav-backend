from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "campusnav-backend"
    environment: str = "development"
    debug: bool = True

    # Database – Supabase PostgreSQL connection string
    # Format: postgresql+psycopg2://user:password@host:port/dbname
    database_url: str = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

    # Supabase project credentials (never expose service_role_key to the frontend)
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # JWT settings (used for verifying / creating tokens)
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS – comma-separated list of allowed origins
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
