from typing import Any
from django.db import models

# Create your models here.
class Users(models.Model):
    msg=models.CharField(max_length=200)
    def __str__(self) -> None:
         return self.msg