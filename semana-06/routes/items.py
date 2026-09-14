import re

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response, status

from config.db import Collection
from models.item import ItemIn, ItemOut, doc_to_itemout

router = APIRouter(prefix="/items", tags=["items"])


def parse_item_id(item_id: str) -> ObjectId:
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    return ObjectId(item_id)


@router.get("", response_model=list[ItemOut])
async def listar_items(
    coll: Collection,
    q: str | None = Query(None, description="Filtro por nombre que contenga q"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    query = {}
    if q:
        # Buscar texto literal, sin interpretar caracteres especiales de regex.
        query["nombre"] = {"$regex": re.escape(q), "$options": "i"}
    cursor = coll.find(query).sort("_id", 1).skip(skip).limit(limit)
    return [doc_to_itemout(doc) async for doc in cursor]


@router.post("", response_model=ItemOut, status_code=201)
async def crear_item(item: ItemIn, coll: Collection):
    res = await coll.insert_one(item.model_dump())
    doc = await coll.find_one({"_id": res.inserted_id})
    return doc_to_itemout(doc)


@router.get("/{item_id}", response_model=ItemOut)
async def obtener_item(item_id: str, coll: Collection):
    doc = await coll.find_one({"_id": parse_item_id(item_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return doc_to_itemout(doc)


@router.put("/{item_id}", response_model=ItemOut)
async def actualizar_item(item_id: str, item: ItemIn, coll: Collection):
    object_id = parse_item_id(item_id)
    res = await coll.update_one(
        {"_id": object_id}, {"$set": item.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    doc = await coll.find_one({"_id": object_id})
    if doc is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return doc_to_itemout(doc)


@router.delete(
    "/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def eliminar_item(item_id: str, coll: Collection):
    res = await coll.delete_one({"_id": parse_item_id(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
