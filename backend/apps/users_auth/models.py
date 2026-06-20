from django.db import models

from core.models import BaseModel


class UserRoleModel(BaseModel):
    name = models.CharField(max_length=55, unique=True)

    class Meta:
        db_table = 'role'
        ordering = ('name',)

    def __str__(self):
        return self.name