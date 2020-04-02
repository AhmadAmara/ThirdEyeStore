from django.db import models

class Category(models.Model):
    catName = models.CharField(primary_key=True,max_length = 200,unique=True)
    isAvtive = models.BooleanField(default=False)


    def __str__(self):
        return self.item + ' | ' + str(self.completed)

class List2(models.Model):
    item = models.CharField(max_length = 200)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return self.item + ' | ' + str(self.completed)


class User(models.Model):
    user_name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, null=True,unique=True)
    password = models.CharField(max_length = 200)


    def __str__(self):
        return self.user_name + ' | ' + self.email + '|' +self.password
        return self.catName + ' | ' + str(self.isAvtive)
