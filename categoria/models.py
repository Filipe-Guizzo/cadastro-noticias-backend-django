from django.db import models

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categoria'
