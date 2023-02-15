from django.db import models
from categoria.models import Categoria
from pessoa.models import Pessoa

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    conteudo = models.CharField(max_length=500)
    imagem = models.ImageField(upload_to="", blank=True, null=True)
    id_categoria = models.IntegerField()
    id_pessoa = models.IntegerField()

    class Meta: 
        managed = False
        db_table = 'noticia'

class NoticiaRelacionamentos(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    conteudo = models.CharField(max_length=500)
    imagem = models.ImageField(upload_to="", blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria,db_column="id_categoria", on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(Pessoa,db_column="id_pessoa", on_delete=models.CASCADE)

    class Meta: 
        managed = False
        db_table = 'noticia'
