from django.db import models

# Create your models here.
class Celebs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    class Meta:
        db_table = "celebs"
    
    def __str__(self):
        return self