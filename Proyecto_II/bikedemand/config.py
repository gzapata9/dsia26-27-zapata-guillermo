from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path

from .errors import DataContractError

try:  # python-dotenv es opcional
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AI_PROVIDERS = ("mock", "hf", "nvidia")


@dataclass(frozen=True)
class Settings:
    # Rutas
    raw_path: Path = PROJECT_ROOT / "data" / "raw" / "hour.csv"
    data_dir: Path = PROJECT_ROOT / "data"
    model_dir: Path = PROJECT_ROOT / "models"
    output_dir: Path = PROJECT_ROOT / "outputs"
    log_level: str = "INFO"

    # Gates de calidad
    # % máximo de filas rechazadas en prepare
    max_error_rate: float = 0.05  
    # R² mínimo en test para promocionar un modelo
    min_r2: float = 0.80  

    # Modelo
    # split temporal, lo posterior es test
    test_from: str = "2012-10-01"  
    random_state: int = 42

    # Ciudad a prever (entrenado con Capital Bikeshare, Washington DC)
    city_name: str = "Washington, DC"
    latitude: float = 38.9072
    longitude: float = -77.0369
    timezone: str = "America/New_York"
    country_code: str = "US"
    subdivision: str = "US-DC"
    horizon_hours: int = 48
    open_data_timeout: float = 15.0

    # Borde IA
    ai_provider: str = "mock"
    hf_token: str | None = field(default=None, repr=False)
    hf_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    nvidia_api_key: str | None = field(default=None, repr=False)
    nvidia_model: str = "nvidia/nemotron-3.5-bolt-e4b"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    ai_timeout: float = 30.0
    ai_max_attempts: int = 3
    ai_max_tokens: int = 500

    @property
    def silver_path(self) -> Path:
        return self.data_dir / "silver" / "hour_clean.csv"

    @property
    def quarantine_path(self) -> Path:
        return self.data_dir / "quarantine" / "rejected.csv"

    @property
    def gold_path(self) -> Path:
        return self.data_dir / "gold" / "training_table.csv"

    @property
    def model_path(self) -> Path:
        return self.model_dir / "demand_model.joblib"

    @property
    def model_card_path(self) -> Path:
        return self.model_dir / "model_card.json"

    def validate(self) -> "Settings":
        if self.ai_provider not in AI_PROVIDERS:
            raise DataContractError(f"AI_PROVIDER='{self.ai_provider}' no válido; usa uno de {AI_PROVIDERS}")
        if self.ai_provider == "hf" and not self.hf_token:
            raise DataContractError("AI_PROVIDER=hf requiere HF_TOKEN en .env")
        if self.ai_provider == "nvidia" and not self.nvidia_api_key:
            raise DataContractError("AI_PROVIDER=nvidia requiere NVIDIA_API_KEY en .env")
        if not 0 <= self.max_error_rate <= 1:
            raise DataContractError("MAX_ERROR_RATE debe estar entre 0 y 1")
        if not 1 <= self.horizon_hours <= 168:
            raise DataContractError("HORIZON_HOURS debe estar entre 1 y 168 (7 días de Open-Meteo)")
        return self

    def with_overrides(self, **overrides) -> "Settings":
        """Aplica los flags de la CLI"""
        return replace(self, **{k: v for k, v in overrides.items() if v is not None}).validate()

    @classmethod
    def from_env(cls, env_file: str | Path | None = PROJECT_ROOT / ".env") -> "Settings":
        if load_dotenv and env_file and Path(env_file).exists():
            load_dotenv(env_file, override=False)
        e = os.environ
        d = cls()

        def num(name: str, default, cast):
            raw = e.get(name)
            if raw in (None, ""):
                return default
            try:
                return cast(raw)
            except ValueError as exc:
                raise DataContractError(f"{name}='{raw}' no es un valor válido") from exc

        return cls(
            raw_path=Path(e.get("RAW_PATH", d.raw_path)),
            data_dir=Path(e.get("DATA_DIR", d.data_dir)),
            model_dir=Path(e.get("MODEL_DIR", d.model_dir)),
            output_dir=Path(e.get("OUTPUT_DIR", d.output_dir)),
            log_level=e.get("LOG_LEVEL", d.log_level).upper(),
            max_error_rate=num("MAX_ERROR_RATE", d.max_error_rate, float),
            min_r2=num("MIN_R2", d.min_r2, float),
            latitude=num("CITY_LAT", d.latitude, float),
            longitude=num("CITY_LON", d.longitude, float),
            horizon_hours=num("HORIZON_HOURS", d.horizon_hours, int),
            ai_provider=e.get("AI_PROVIDER", d.ai_provider).strip().lower(),
            hf_token=e.get("HF_TOKEN") or None,
            hf_model=e.get("HF_MODEL") or d.hf_model,
            nvidia_api_key=e.get("NVIDIA_API_KEY") or None,
            nvidia_model=e.get("NVIDIA_MODEL") or d.nvidia_model,
            ai_timeout=num("AI_TIMEOUT", d.ai_timeout, float),
        ).validate()
