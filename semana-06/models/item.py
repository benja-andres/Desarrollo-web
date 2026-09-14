from pydantic import BaseModel, Field


class Item(BaseModel):
    nombre: str = Field(min_length=1, description="Nombre del producto")
    precio: float = Field(gt=0, allow_inf_nan=False, description="Precio mayor que cero")
    tags: list[str] = Field(default_factory=list)
    activo: bool = True


class ItemIn(Item):
    """Datos de entrada; MongoDB genera el identificador."""


class ItemOut(Item):
    id: str


def doc_to_itemout(doc: dict) -> ItemOut:
    return ItemOut(
        id=str(doc["_id"]),
        nombre=doc["nombre"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        activo=doc.get("activo", True),
    )
