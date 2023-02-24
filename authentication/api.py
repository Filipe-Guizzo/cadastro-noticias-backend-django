from ninja import Router, Schema
from pessoa.models import Pessoa
import bcrypt

class LoginSchema(Schema):
    token:str

class LoginSchemaIn(Schema):
    email:str
    senha: str

class MessageSchema(Schema):
    message:str
    status: int

router = Router()

@router.post("/login", response={200:LoginSchema,401:MessageSchema})
def login(request, payload: LoginSchemaIn):
    json_data = payload.dict()
    
    email = json_data["email"]
    senha = json_data["senha"]
    
    try:
        usuario = Pessoa.objects.get(email=email)
        
        if bcrypt.checkpw(senha.encode("utf-8"), usuario.senha.encode("utf-8")):
                return 200,{
                    "token":usuario.token,
                    "id_usuario": usuario.id
                }
        else:
            return 401,{
                "message": "E-mail ou senha incorreto",
                "status": 401
            }
    except:
        return 401,{
            "message": "E-mail ou senha incorreto",
            "status": 401
        }
        