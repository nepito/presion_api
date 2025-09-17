import uuid
from typing import List, Dict

from fastapi import FastAPI, HTTPException, status
from .schema import PresionArterialCreate, PresionArterialResponse, PresionArterialUpdate

# --- Configuración de la Aplicación ---
app = FastAPI(
    title="API de Presión Arterial",
    description="Una API para registrar y consultar lecturas de presión arterial. 🩺❤️",
    version="1.0.0",
)

# --- Simulación de Base de Datos ---
# En una aplicación real, esto sería reemplazado por una conexión a una base de datos
# como PostgreSQL o MongoDB, y la lógica estaría en un archivo `crud.py`.
db_lecturas: Dict[str, PresionArterialResponse] = {}


# --- Endpoints de la API ---


@app.post(
    "/presiones",
    response_model=PresionArterialResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Lecturas"],
)
def registrar_lectura(lectura_in: PresionArterialCreate):
    """
    Registra una nueva lectura de presión arterial.

    - **Recibe**: Los datos de la medición.
    - **Crea**: Un ID único para el registro.
    - **Devuelve**: El registro completo, incluyendo su nuevo ID.
    """
    lectura_id = str(uuid.uuid4())
    nueva_lectura = PresionArterialResponse(id=lectura_id, **lectura_in.model_dump())
    db_lecturas[lectura_id] = nueva_lectura
    return nueva_lectura


@app.get("/presiones", response_model=List[PresionArterialResponse], tags=["Lecturas"])
def obtener_todas_las_lecturas(skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de todas las lecturas de presión arterial registradas.
    Permite paginación a través de los parámetros `skip` y `limit`.
    """
    lecturas = list(db_lecturas.values())
    return lecturas[skip : skip + limit]


@app.get("/presiones/{lectura_id}", response_model=PresionArterialResponse, tags=["Lecturas"])
def obtener_lectura_por_id(lectura_id: str):
    """
    Obtiene una lectura específica por su ID.
    Si la lectura no existe, devuelve un error 404.
    """
    lectura = db_lecturas.get(lectura_id)
    if not lectura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada.")
    return lectura


@app.put("/presiones/{lectura_id}", response_model=PresionArterialResponse, tags=["Lecturas"])
def actualizar_lectura(lectura_id: str, lectura_update: PresionArterialUpdate):
    """
    Actualiza una lectura de presión arterial existente por su ID.

    Solo se actualizarán los campos proporcionados en el cuerpo de la solicitud.
    """
    lectura_existente = db_lecturas.get(lectura_id)
    if not lectura_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada.")

    # Convertimos el modelo Pydantic a un diccionario para poder actualizarlo
    update_data = lectura_update.model_dump(exclude_unset=True)
    lectura_actualizada = lectura_existente.model_copy(update=update_data)

    db_lecturas[lectura_id] = lectura_actualizada
    return lectura_actualizada


@app.delete("/presiones/{lectura_id}", status_code=status.HTTP_200_OK, tags=["Lecturas"])
def eliminar_lectura(lectura_id: str):
    """
    Elimina una lectura de presión arterial por su ID.
    """
    if lectura_id not in db_lecturas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lectura no encontrada.")

    del db_lecturas[lectura_id]
    return {"mensaje": "Lectura eliminada exitosamente."}
