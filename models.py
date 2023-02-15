# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categoria'


class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.CharField(max_length=500)
    imagem = models.CharField(max_length=500, blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='id_categoria')
    id_pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING, db_column='id_pessoa')

    class Meta:
        managed = False
        db_table = 'noticia'


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=500)
    imagem = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'pessoa'
