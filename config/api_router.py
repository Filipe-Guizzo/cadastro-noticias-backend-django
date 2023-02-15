from ninja import NinjaAPI
from pessoa.api import router as pessoas, Pessoa
from categoria.api import router as categorias
from noticia.api import router as noticias
from authentication.api import router as auth
from ninja.security import HttpBearer

api = NinjaAPI()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            Pessoa.objects.get(token=token)
            return token
        except:
            return False

api.add_router("auth", auth)
api.add_router("pessoas", pessoas)
api.add_router("categorias", categorias, auth=AuthBearer())
api.add_router("noticias", noticias, auth=AuthBearer())
