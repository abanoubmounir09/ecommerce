from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


#path for imag
def upload_path(instance,filename):
    return '/media'.join(['product',str(instance.PRDName),filename])

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.PRDName), filename])
    
class Product(models.Model):
    PRDName = models.CharField(max_length=100 , verbose_name=_("Product Name "))
    # PRDRate = models.ForeignKey('Rating' , on_delete=models.CASCADE ,blank=True, null=True , verbose_name=_("PRDRate"))
    PRDCategory = models.ForeignKey('Category' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Category "))
    PRDDesc = models.TextField(verbose_name=_("Description"))
    PRDQuantity= models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)],null=True,default=None)

    PRDImage = models.ImageField(upload_to=nameFile , verbose_name=_("Image") , blank=True, null=True)
     
    PRDPrice = models.FloatField( verbose_name=_("Price"))
    PRDDiscountPrice = models.FloatField(verbose_name=_("Discount Price"))
    PRDCost = models.FloatField(verbose_name=_("Cost"))
    PRDCreatedNow = models.DateTimeField(auto_now_add=True,verbose_name=_("Created in"))
    
    def __str__(self):
        return self.PRDName


    def no_of_rating(self):
        ratings=Rating.objects.filter(RATProduct=self)
        return len(ratings)


    def avg_of_rating(self):
        sum=0
        ratings=Rating.objects.filter(RATProduct=self)
        for rating in ratings:
            sum+=rating.stars
            if len(ratings)>0:
                return sum/len(ratings)
            else:
                return 0


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
    CATDesc = models.TextField( verbose_name=_("Description"),null=True)
    CATImg = models.ImageField(upload_to='category/' , verbose_name=_("Image"),null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.CATName


class Order(models.Model):
     Orderproduct = models.ForeignKey(Product , on_delete=models.CASCADE, verbose_name=_("productref"), blank=True, null=True )
     order_user=models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True)
     order_quantity=models.IntegerField(null=True)  
class Rating(models.Model):
    RATProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("RATEProduct"))
    RATUser = models.ForeignKey(User ,on_delete=models.CASCADE , verbose_name=_("RATEUser"))
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
 


#table between owner and product
class OwnerProduct(models.Model):
    OwnerUser=models.ForeignKey(User ,on_delete=models.CASCADE , verbose_name=_("OwnerUser"))
    Ownerproduct = models.ForeignKey(Product ,on_delete=models.CASCADE , verbose_name=_("OwnerProduct"),related_name='tracks')
    OwnerQuantity= models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)],null=True,default=None)

    