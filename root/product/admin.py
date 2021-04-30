from django.contrib import admin

# Register your models here.


from product.models import ProductImage , Category ,Product,Order,Rating,OwnerProduct,Favorite


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(OwnerProduct)
admin.site.register(Favorite)
