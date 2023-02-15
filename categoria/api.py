from ninja import Router, Schema
from typing import List
from categoria.models import Categoria
from ninja.orm import create_schema

CategoriaSchema = create_schema(Categoria)
CategoriaSchemaIn = create_schema(Categoria, exclude=["id"])

class MessageSchema(Schema):
    message:str
    status: int

router = Router()

@router.get("/", response=List[CategoriaSchema])
def get_all(request):
    objetos = Categoria.objects.all()
    return objetos

@router.get("/{id}/", response=CategoriaSchema)
def get_by_id(request, id:int):
    objeto = Categoria.objects.get(id=id)
    return objeto

@router.post("/", response=CategoriaSchema)
def create(request, payload:CategoriaSchemaIn):
    json_data = payload.dict()
    objeto = Categoria.objects.create(**json_data)
    return objeto

@router.put("/{id}/", response=CategoriaSchema)
def update(request, id: int, payload:CategoriaSchemaIn):
    json_data = payload.dict()
    Categoria.objects.filter(id=id).update(**json_data)
    objeto = Categoria.objects.get(id=id)
    return objeto

@router.delete("/{id}/", response=MessageSchema)
def delete(request, id: int):
    objeto = Categoria.objects.get(id=id)
    objeto.delete()
    return {
        "message": "Deletado com sucesso",
        "status": 200
    }