from django.db import models
# Create your models here.


class OJ(models.Model):
    name = models.CharField(max_length=20, unique=True)
    max_problem_id = models.IntegerField()

    def update(self, new_id):
        self.max_problem_id = new_id

    class Meta:
        db_table = 'OJ'

    def __str__(self):
        return self.name
