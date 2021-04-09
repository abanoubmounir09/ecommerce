from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator

from .models import Product,Category
from .forms import addproductform

#serialize
from .serializers import productSerializer
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response




#create class
class productViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productSerializer
    #permission_classes = [permissions.IsAuthenticated]

# create get all api
@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Product.objects.all()
        serializer = productSerializer(snippets, many=True)
        return Response(serializer.data)

# create get api
@api_view(['GET', 'POST'])
def snippet_list_item(request,pk):
    if request.method == 'GET':
        snippets = Product.objects.filter(id=pk)
        serializer = productSerializer(snippets, many=True)
        return Response(serializer.data)




# Create your views here.
def home(request):
    list_samsung = Product.objects.filter(PRDCategory__CATName='samsung')
    paginator = Paginator(list_samsung, 2) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pagination.html', {'page_obj': page_obj})

    """category_list= Category.objects.filter(product__PRDName='note 11')
    print('**************',category_list)
    print(list_samsung)
    return HttpResponse(list_samsung.first())"""



def addproduct(request):
    if request.method == 'POST':
        obproduct=Product()
        form = addproductform(request.POST,request.FILES)
        if form.is_valid():
            newproduct = form.save(commit=False)
            newproduct.save()
        return  HttpResponse('item added')

    else:
         form = addproductform()
         return render(request,'new_product.html',{'form':form})


"""
@login
def addtocard(request):
    loginuser = request.user
    productid = itemId
    objectfromOrdertable??

"""

#function to display product details
"""
def product_details(request):
    products=Product.objects.get(id=productid)
    return render(request,"detail.html",{'products':products})
    """


    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def showproduct(request):
    obj=Product.objects.all()
    return render(request,'home.html',{'data':obj})
