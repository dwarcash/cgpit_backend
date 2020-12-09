from django.db import models

class ResultDetails(models.Model):
    resultID  = models.AutoField(primary_key = True)
    


    def __str__(self):
        return f'{self.resultID} - {self.resultID}'