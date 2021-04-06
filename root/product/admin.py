from django.contrib import admin

# Register your models here.


from product.models import ProductImage , Category ,Product


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
