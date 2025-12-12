from django.db import models

# Create your models here.

class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    semestre = models.IntegerField()
    profesor = models.CharField(max_length=200)
    comentarios = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = "Materias"
    
    def __str__(self):
        return self.nombre