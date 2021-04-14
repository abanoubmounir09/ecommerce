from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Product(models.Model):
    PRDName = models.CharField(max_length=100 , verbose_name=_("Product Name "))
    PRDRate = models.ForeignKey('Rating' , on_delete=models.CASCADE ,blank=True, null=True , verbose_name=_("PRDRate"))
    PRDCategory = models.ForeignKey('Category' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Category "))
    #PRDBrand = models.ForeignKey('settings.Brand' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    PRDDesc = models.TextField(verbose_name=_("Description"))
    PRDImage = models.ImageField(upload_to='prodcut/' , verbose_name=_("Image") , blank=True, null=True)
    PRDPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("Price"))
    PRDDiscountPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("Discount Price"))    
    PRDCost = models.DecimalField(max_digits=5 , decimal_places=2 , verbose_name=_("Cost"))
    PRDCreatedNow = models.DateTimeField(auto_now_add=True,verbose_name=_("Created in"))
    
    def __str__(self):
        return self.PRDName

#----------------------------------------

class ProductImage(models.Model):
    PRDIProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("Product"))
    PRDIImage = models.ImageField(upload_to='prodcut/' , verbose_name=_("Image"))
    def __str__(self):
        return str(self.PRDIProduct)


#----------------------------------------
class Category(models.Model):
    CATName = models.CharField(max_length=50 , verbose_name=_("Name"))
    CATParent = models.ForeignKey('self' ,limit_choices_to={'CATParent__isnull' : True}, verbose_name=_("Main Category"), on_delete=models.CASCADE , blank=True, null=True)
    CATDesc = models.TextField( verbose_name=_("Description"))
    CATImg = models.ImageField(upload_to='category/' , verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.CATName


class Order(models.Model):
     Orderuser = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name=_("userref"),blank=True, null=True)
     Orderproduct = models.ForeignKey(Product , on_delete=models.CASCADE, verbose_name=_("productref"), blank=True, null=True )
     

     
class Rating(models.Model):
    RATProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("RATEProduct"))
    RATUser = models.ForeignKey(User ,on_delete=models.CASCADE , verbose_name=_("RATEUser"))
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    # def __str__(self):
    #     return str(self.RATProduct__PRDName)


#table between owner and product
class OwnerProduct(models.Model):
    OwnerUser=models.ForeignKey(User ,on_delete=models.CASCADE , verbose_name=_("OwnerUser"))
    OwnerProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("OwnerProduct"))
    OwnerQuantity = models.IntegerField(Product)