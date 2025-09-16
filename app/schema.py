# schemas.py

from datetime import date, time, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class PresionArterialBase(BaseModel):
    """Modelo base con los campos comunes para una lectura de presión arterial."""
    sistolica: int = Field(..., ge=0, le=300, description="Presión sistólica en mmHg.")
    diastolica: int = Field(..., ge=0, le=200, description="Presión diastólica en mmHg.")
    pulso: int = Field(..., ge=0, le=250, description="Frecuencia cardíaca en pulsaciones por minuto.")
    fecha_medicion: date = Field(default_factory=date.today)
    hora_medicion: time = Field(default_factory=lambda: datetime.now().time())
    notas: Optional[str] = Field(None, description="Notas adicionales sobre la medición.")
    etiquetas: Optional[List[str]] = Field(None, description="Lista de etiquetas descriptivas.")
    
    # Proporciona un ejemplo para la documentación de la API
    class Config:
        json_schema_extra = {
            "example": {
                "sistolica": 120,
                "diastolica": 80,
                "pulso": 75,
                "fecha_medicion": "2025-09-16",
                "hora_medicion": "08:30:00",
                "notas": "Medición en ayunas, después de 10 minutos de reposo.",
                "etiquetas": ["mañana", "reposo"]
            }
        }

class PresionArterialCreate(PresionArterialBase):
    """
    Modelo para crear una nueva lectura.
    Actualmente no tiene campos adicionales, pero está preparado para escalar
    (ej. añadiendo un 'user_id').
    """
    pass

class PresionArterialUpdate(BaseModel):
    """
    Modelo para actualizar una lectura existente. Todos los campos son opcionales
    para permitir actualizaciones parciales (PATCH/PUT).
    """
    sistolica: Optional[int] = Field(None, ge=0, le=300)
    diastolica: Optional[int] = Field(None, ge=0, le=200)
    pulso: Optional[int] = Field(None, ge=0, le=250)
    notas: Optional[str] = None
    etiquetas: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "sistolica": 125,
                "notas": "Medición después de caminar."
            }
        }


class PresionArterialResponse(PresionArterialBase):
    """Modelo para las respuestas de la API, incluye el ID único del registro."""
    id: str = Field(description="Identificador único de la lectura.")

    class Config:
        # Pydantic v2 usa 'json_schema_extra', en v1 era 'schema_extra'
        # Este ejemplo es compatible con ambas versiones
        json_schema_extra = {
            "example": {
                "id": "e7b2a3c1-f9d5-4a8e-8c6f-3b5d1a2e9f0c",
                "sistolica": 120,
                "diastolica": 80,
                "pulso": 75,
                "fecha_medicion": "2025-09-16",
                "hora_medicion": "08:30:00",
                "notas": "Medición en ayunas.",
                "etiquetas": ["mañana", "reposo"]
            }
        }
        # Habilita el modo ORM para que Pydantic pueda leer datos de objetos
        # con atributos (útil si se integra con un ORM como SQLAlchemy).
        from_attributes = True