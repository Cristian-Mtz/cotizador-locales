from __future__ import annotations

import json
from typing import Any, List, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="cotizador-locales", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    environment: Literal["local", "dev", "prod", "test"] = Field(default="local", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api", alias="API_V1_PREFIX")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:4200"], alias="CORS_ORIGINS")

    mongodb_uri: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URI")
    mongodb_db: str = Field(default="app_db", alias="MONGODB_DB")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors(cls, v: Any) -> List[str]:
        if v is None:
            return ["http://localhost:4200"]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return ["http://localhost:4200"]
            if s.startswith("["):
                try:
                    data = json.loads(s)
                    if isinstance(data, list):
                        return [str(x).strip() for x in data if str(x).strip()]
                except Exception:
                    pass
            return [i.strip() for i in s.split(",") if i.strip()]
        return ["http://localhost:4200"]


settings = Settings()
