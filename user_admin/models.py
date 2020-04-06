from django.db import models

class Category(models.Model):
    catName = models.CharField(max_length = 200,unique=True)
    isAvtive = models.BooleanField(default=True)

    def __str__(self):
        return self.catName + ' | ' + str(self.isAvtive)


class User(models.Model):
    email = models.EmailField(primary_key=True, max_length = 200, unique=True)
    password = models.CharField(max_length = 200)
    typ = models.CharField(max_length = 200,default='customer')


    def __str__(self):
        return  self.email + '|' +self.password


class Product(models.Model):
    category = models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    Name= models.CharField(max_length=200,unique=True)
    Weight = models.FloatField()
    price = models.FloatField()
    Quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Name +' | ' +str(self.category) + ' | ' +str(self.price) + ' | ' +str(self.Quantity) +' | ' + str(self.Weight)




class Cart(models.Model):
    User_em = models.ForeignKey(User,on_delete=models.CASCADE)
    isCheckout = models.BooleanField(default=False)

    def __str__(self):
        return str(self.User_em) + ' | ' + str(self.isCheckout)


class Order_Line(models.Model):
    CartId = models.ForeignKey(Cart,default=1,on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product,default=1,on_delete=models.CASCADE)
    price = models.FloatField()
    Quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.CartId) +' | ' +str(self.ProductID) + ' | ' +str(self.price) + ' | ' +str(self.Quantity) 
