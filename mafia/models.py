from django.db import models

# Create your models here.

class Role(models.Model):
    
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.name

class Gamers(models.Model):
    
    name = models.CharField(max_length=30)
    role = models.ForeignKey(Role,on_delete=models.CASCADE , blank=True, null=True)
    is_dead = models.BooleanField(default=False)
    is_linchead = models.BooleanField(default=False) #додав

    def __str__(self) -> str:
        return self.name




