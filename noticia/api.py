from ninja import Router, Schema, File
from typing import List
from noticia.models import Noticia, NoticiaRelacionamentos
from ninja.orm import create_schema
from categoria.api import Categoria,CategoriaSchema
from pessoa.api import Pessoa, PessoaSchema
from ninja.files import UploadedFile
from django.db.models import Q

NoticiaSchema = create_schema(Noticia)
NoticiaSchemaIn = create_schema(Noticia, exclude=["id", "imagem"])

class NoticiaRelacionamentosSchema(Schema):
    id:int
    titulo: str
    conteudo: str
    id_categoria: int
    id_pessoa: int
    imagem: str = None
    pessoa: PessoaSchema
    categoria: CategoriaSchema

class MessageSchema(Schema):
    message:str
    status: int

router = Router()

@router.get("/", response=List[NoticiaRelacionamentosSchema])
def get_all(request):
    objetos = Noticia.objects.all()
    response = []
    for noticia in objetos:
        noticia_serializer = NoticiaSchema.from_orm(noticia).dict()
        categoria = Categoria.objects.get(id=noticia.id_categoria)
        noticia_serializer["categoria"] = categoria
        pessoa = Pessoa.objects.get(id=noticia.id_pessoa)
        noticia_serializer["pessoa"] = pessoa
        response.append(noticia_serializer)
    return response

@router.get("/{id}/", response=NoticiaRelacionamentosSchema)
def get_by_id(request, id:int):
    objeto = Noticia.objects.get(id=id)
    noticia = objeto
    noticia_serializer = NoticiaSchema.from_orm(noticia).dict()
    categoria = Categoria.objects.get(id=noticia.id_categoria)
    noticia_serializer["categoria"] = categoria
    pessoa = Pessoa.objects.get(id=noticia.id_pessoa)
    noticia_serializer["pessoa"] = pessoa
    return noticia_serializer

@router.post("/", response=NoticiaSchema)
def create(request, payload:NoticiaSchemaIn):
    json_data = payload.dict()
    objeto = Noticia.objects.create(**json_data)
    return objeto

@router.put("/{id}/", response=NoticiaSchema)
def update(request, id: int, payload:NoticiaSchemaIn):
    json_data = payload.dict()
    Noticia.objects.filter(id=id).update(**json_data)
    objeto = Noticia.objects.get(id=id)
    return objeto

@router.delete("/{id}/", response=MessageSchema)
def delete(request, id: int):
    objeto = Noticia.objects.get(id=id)
    objeto.delete()
    return {
        "message": "Deletado com sucesso",
        "status": 200
    }
    
@router.post("/{id}/upload-file", response=NoticiaSchema)
def upload_file(request, id: int,  file:UploadedFile = File(...)):
    objeto = Noticia.objects.get(id=id)
    objeto.imagem = file
    objeto.save()
    return objeto

@router.get("/search/{param}/", response=List[NoticiaRelacionamentosSchema])
def search(request, param:str):
    objetos = NoticiaRelacionamentos.objects.filter(
        Q(titulo__istartswith=param)|
        Q(conteudo__istartswith=param)|
        Q(id_categoria__nome__istartswith=param)|
        Q(id_pessoa__nome__istartswith=param)
    )
    response = []
    for noticia_relacionamentos in objetos:
        noticia = Noticia.objects.get(id=noticia_relacionamentos.id)
        noticia_serializer = NoticiaSchema.from_orm(noticia).dict()
        categoria = Categoria.objects.get(id=noticia.id_categoria)
        noticia_serializer["categoria"] = categoria
        pessoa = Pessoa.objects.get(id=noticia.id_pessoa)
        noticia_serializer["pessoa"] = pessoa
        response.append(noticia_serializer)
    return response