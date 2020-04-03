from django.db import models

class Category(models.Model):
    catName = models.CharField(primary_key=True,max_length = 200,unique=True)
    isAvtive = models.BooleanField(default=False)


    def __str__(self):
        return self.catName + ' | ' + str(self.isAvtive)


class User(models.Model):
    user_name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, null=True,unique=True)
    password = models.CharField(max_length = 200)


    def __str__(self):
        return self.user_name + ' | ' + self.email + '|' +self.password

class Product(models.Model): 
    #ProductID = models.CharField(primary_key=True,max_length = 200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    ProductName= models.CharField(max_length=200)
    Wight =  models.FloatField()
    price = models.FloatField()
    Quantiy = models.IntegerField(default=0)
    def __str__(self):
        return self.title + ' | ' +str(self.category) + ' | ' +str(self.price) + ' | ' +str(self.qty) + self.description

