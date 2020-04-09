from django.db import models
from user_admin.fields import IntegerRangeField

class Category(models.Model):
    catName = models.CharField(max_length = 200,unique=True)
    isAvtive = models.BooleanField(default=True)

    def __str__(self):
        return self.catName + ' | ' + str(self.isAvtive)


class User(models.Model):
    email = models.EmailField(primary_key=True, max_length = 200, unique=True)
    password = models.CharField(max_length = 200)
    typ = models.CharField(max_length = 200,default='customer')

    class Meta:
        ordering = ['typ']

    def __str__(self):
        return  self.email + '|' +self.password+'|'+self.typ


class Product(models.Model):
    category = models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    Name= models.CharField(max_length=200,unique=True)
    Weight = models.FloatField()
    price = models.FloatField()
    Quantity = models.IntegerField(default=0)

    packge_sale = models.ManyToManyField('PackgeSale', through='ProductAndPackgeMemberShip')
    product_discout = models.ManyToManyField('ProductDiscount', through='ProductAndDiscountMemberShip')

    def __str__(self):
        return self.Name +' | ' +str(self.category) + ' | ' +str(self.price) + ' | ' +str(self.Quantity) +' | ' + str(self.Weight)




class Cart(models.Model):
    User_em = models.ForeignKey(User,on_delete=models.CASCADE)
    dt=models.DateTimeField(auto_now=True)
    total_price = models.FloatField(default=0)
    isCheckout = models.BooleanField(default=False)

    class Meta:
        ordering = ['dt']
        
    def __str__(self):
        return str(self.User_em) + ' | ' + str(self.dt)+ ' | ' + str(self.total_price)+ ' | ' + str(self.isCheckout)



class Order_Line(models.Model):
    CartId = models.ForeignKey(Cart,default=1,on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product,default=1,on_delete=models.CASCADE)
    price = models.FloatField()
    Quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.CartId) +' | ' +str(self.ProductID) + ' | ' +str(self.price) + ' | ' +str(self.Quantity) 


<<<<<<< HEAD
=======

>>>>>>> added models for discount and sales
###################################### Sales And Discounts #######################################################


class PackgeSale(models.Model):
    title = models.CharField(max_length=128, unique=True)
    final_price = models.FloatField()
    end_date = models.DateField()
    products = models.ManyToManyField('Product', through='ProductAndPackgeMemberShip')

    def __str__(self):
        return self.title + '|' + str(self.final_price) + '|' + str(self.end_date)


class ProductAndPackgeMemberShip(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package_sale =  models.ForeignKey(PackgeSale, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product.Name) + " in sale " + str(self.package_sale.title)


class ProductDiscount(models.Model):
    title = models.CharField(max_length=128, unique=True)
    discount_percent = IntegerRangeField(min_value=0, max_value=100)
    products = models.ManyToManyField('Product', through='ProductAndDiscountMemberShip')

    def __str__(self):
        return self.title + '|' + str(self.discount_percent)


class ProductAndDiscountMemberShip(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_discount =  models.ForeignKey(ProductDiscount, on_delete=models.CASCADE)
    end_date = models.DateField()

    def __str__(self):
        return str(self.product.Name) + " in discount " + str(self.product_discount.title) + " until " + str(self.end_date)