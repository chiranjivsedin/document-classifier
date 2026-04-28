from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Document Classifier AI"
    APP_VERSION: str = "0.1.0"

    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma3:4b"
    OCR_ENGINE: str = "rapidocr"
    DOCUMENT_CATEGORIES: list[str] = [
        "invoice",
        "contract",
        "id_proof",
        "report",
        "other",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
