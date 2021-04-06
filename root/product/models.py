from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Product(models.Model):
    PRDName = models.CharField(max_length=100 , verbose_name=_("Product Name "))
    PRDCategory = models.ForeignKey('Category' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Category "))
    #PRDBrand = models.ForeignKey('settings.Brand' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    PRDDesc = models.TextField(verbose_name=_("Description"))
    PRDImage = models.ImageField(upload_to='prodcut/' , verbose_name=_("Image") , blank=True, null=True)
    PRDPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("Price"))
    PRDDiscountPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("Discount Price"))    
    PRDCost = models.DecimalField(max_digits=5 , decimal_places=2 , verbose_name=_("Cost"))
    PRDCreated = models.DateTimeField(verbose_name=_("Created At"))
    
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



