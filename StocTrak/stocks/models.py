from django.db import models
# from config import settings

# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker

