from django.db import models

class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=500)
    imagem = models.ImageField(upload_to="", blank=True, null=True)
    token = models.CharField(max_length=500)
    telefone = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'pessoa'
