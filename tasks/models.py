from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Task(models.Model):

    STATUS = (
        ('doing','Doing'),
        ('done', 'Done')
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    done = models.CharField(
        max_length=5,
        choices=STATUS,  
    )
    #chave estrangeira, que pode ser usado para filtrar informação de cada usuario
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.title)
        