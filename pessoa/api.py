from ninja import Router, Schema, File
from typing import List
from pessoa.models import Pessoa
from ninja.orm import create_schema
import bcrypt
import jwt
from ninja.files import UploadedFile
from ninja.security import HttpBearer
import random
from twilio.rest import Client

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            Pessoa.objects.get(token=token)
            return token
        except:
            return False

PessoaSchema = create_schema(Pessoa)
PessoaSchemaIn = create_schema(Pessoa, exclude=["id", "token", "imagem"])

class EnviarSmsSchema(Schema):
    codigo:int
    id_pessoa: int

class EnviarSmsSchemaIn(Schema):
    email:str

class ReenviarSmsSchemaIn(Schema):
    codigo: int
    id_pessoa: int

class ResetarSenhaSchemaIn(Schema):
    senha: str
    id_pessoa: int


class MessageSchema(Schema):
    message:str
    status: int

router = Router()

@router.post("/enviar-sms/", response={200:EnviarSmsSchema, 404:MessageSchema})
def enviar_sms(request, payload:EnviarSmsSchemaIn):
        json_data = payload.dict()
        email = json_data['email']
        pessoa = Pessoa.objects.get(email=email)
        codigo = random.randint(1000, 9999)
        numero = ''.join(e for e in pessoa.telefone if e.isalnum())
        
        account_sid = "AC04f62018059822ba5b7930b7a5bfeffc"
        auth_token  = "a1fd63bdefaae89eca9c3181c144e8e4"

        client = Client(account_sid, auth_token)

        client.messages.create(to=f"+55{numero}", from_="+19035467693",body=f"Codigo de recuperação de senha: {codigo}")
        
        return 200,{
            "codigo": codigo,
            "id_pessoa": pessoa.id
        }


@router.post("/reenviar-sms/", response={200:EnviarSmsSchema, 400:MessageSchema})
def reenviar_sms(request, payload:ReenviarSmsSchemaIn):
    json_data = payload.dict()
    id_pessoa = json_data['id_pessoa']
    codigo = json_data['codigo']
    try:
        pessoa = Pessoa.objects.get(id=id_pessoa)
        numero = ''.join(e for e in pessoa.telefone if e.isalnum())
        
        account_sid = "AC04f62018059822ba5b7930b7a5bfeffc"
        auth_token  = "7f167cf408a10ac237f0e290c300eed9"

        client = Client(account_sid, auth_token)

        client.messages.create(to=f"+55{numero}", from_="+19035467693",body=f"Codigo de recuperação de senha: {codigo}")
        
        return 200,{
            "codigo": codigo,
            "id_pessoa": pessoa.id
        }
    except:
        return 400,{
            "message": "Erro ao reenviar codigo",
            "status": 400
        }

@router.post("/resetar-senha/", response={200:MessageSchema, 400:MessageSchema})
def resetar_senha(request, payload:ResetarSenhaSchemaIn):
    json_data = payload.dict()
    id_pessoa = json_data['id_pessoa']
    try:
        pessoa = Pessoa.objects.get(id=id_pessoa)
        senha =  json_data['senha'].encode('ascii')
        senha_hash =  bcrypt.hashpw(senha,bcrypt.gensalt())
        pessoa.senha = senha_hash
        pessoa.save()
        return 200,{
            "message": "Senha alterada com sucesso!",
            "status": 200
        }
    except:
        return 400,{
            "message": "Erro ao reenviar codigo",
            "status": 400
        }


@router.get("/", response=List[PessoaSchema], auth=AuthBearer())
def get_all(request):
    objetos = Pessoa.objects.all()
    return objetos

@router.get("/{id}/", response=PessoaSchema, auth=AuthBearer())
def get_by_id(request, id:int):
    objeto = Pessoa.objects.get(id=id)
    return objeto

@router.post("/", response=PessoaSchema)
def create(request, payload:PessoaSchemaIn):
    json_data = payload.dict()
    #senha criptografada
    senha =  json_data['senha'].encode('ascii')
    senha_hash =  bcrypt.hashpw(senha,bcrypt.gensalt())
    json_data["senha"] = senha_hash.decode("utf-8")
    #gerando token jwt
    token = jwt.encode({"nome": json_data["nome"] }, senha_hash, algorithm="HS256")
    json_data["token"] = token
    objeto = Pessoa.objects.create(**json_data)
    return objeto

@router.put("/{id}/", response=PessoaSchema, auth=AuthBearer())
def update(request, id: int, payload:PessoaSchemaIn):
    json_data = payload.dict()
    #senha criptografada
    senha =  json_data['senha'].encode('ascii')
    senha_hash =  bcrypt.hashpw(senha,bcrypt.gensalt())
    json_data["senha"] = senha_hash.decode("utf-8")
    Pessoa.objects.filter(id=id).update(**json_data)
    objeto = Pessoa.objects.get(id=id)
    return objeto

@router.delete("/{id}/", response=MessageSchema, auth=AuthBearer())
def delete(request, id: int):
    objeto = Pessoa.objects.get(id=id)
    objeto.delete()
    return {
        "message": "Deletado com sucesso",
        "status": 200
    }

@router.post("/{id}/upload-file", response=PessoaSchema, auth=AuthBearer())
def upload_file(request, id: int,  file:UploadedFile = File(...)):
    objeto = Pessoa.objects.get(id=id)
    objeto.imagem = file
    objeto.save()
    return objeto