from django.db import models

class Category(models.Model):
    catName = models.CharField(primary_key=True,max_length = 200,unique=True)
    isAvtive = models.BooleanField(default=False)

    def __str__(self):
        return self.catName + ' | ' + str(self.isAvtive)


class User(models.Model):
    email = models.EmailField(primary_key=True, max_length = 200, unique=True)
    password = models.CharField(max_length = 200)


    def __str__(self):
        return  self.email + '|' +self.password


