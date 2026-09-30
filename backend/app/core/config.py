from pathlib import Path
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = 'development'
    DATABASE_URL: str = 'postgresql+psycopg2://janvastu:janvastu_pass@localhost:5432/janvastu'
    SECRET_KEY: str = 'development-only-change-this-secret-before-deployment'
    CORS_ORIGINS: str = 'http://localhost:5173,http://127.0.0.1:5173'
    MINIO_ENDPOINT: str = 'localhost:9000'
    MINIO_ACCESS_KEY: str = ''
    MINIO_SECRET_KEY: str = ''
    MINIO_BUCKET: str = 'janvastu-media'
    MINIO_SECURE: bool = False
    MINIO_REGION: str = ''
    NOMINATIM_BASE_URL: str = 'https://nominatim.openstreetmap.org'
    NOMINATIM_USER_AGENT: str = 'JanVastu/1.0 (local civic prototype)'
    MOCK_OTP_ENABLED: bool = True
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/api/v1/auth/google/callback'
    FRONTEND_URL: str = 'http://localhost:5173'
    MAX_UPLOAD_BYTES: int = 20 * 1024 * 1024
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / '.env', extra='ignore')

    @model_validator(mode='after')
    def production_settings(self):
        if self.DATABASE_URL.startswith('postgres://'):
            self.DATABASE_URL = self.DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        if self.APP_ENV == 'production' and (len(self.SECRET_KEY) < 32 or self.SECRET_KEY.startswith(('development-', 'unsafe-', 'change_me'))):
            raise ValueError('Production requires a random SECRET_KEY of at least 32 characters')
        if self.APP_ENV == 'production' and self.MOCK_OTP_ENABLED:
            raise ValueError('Mock OTP is for demo environments only; use APP_ENV=demo for the hackathon')
        return self

settings = Settings()
