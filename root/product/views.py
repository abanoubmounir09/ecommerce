from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator
from .models import Product,Category,Rating,Order
from .forms import addproductform
from django.contrib.auth.models import User
#serialize
from .serializers import productSerializer, categorySerializer, orderSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.http import HttpResponse
from django.db.models import Q

# test for all parameters
@api_view(['POST'])
def query_test(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        category = body['category'] #select items from dictionary by name
        prodname= body['Prodname'] 
        # print("*******category*********",category)
        priceSTR = body['price'] 
        # prictInt:int; 
        query = Q()
        query= Product.objects.all()
        if(category!=""):
            qtest= Product.objects.filter(Q(PRDCategory__CATName=category))
            if(len(qtest)!= 0):
                query &= qtest
        if(prodname!=""):
            qtest= Product.objects.filter(Q(PRDName=prodname))
            if(len(qtest)!= 0):
                query &=qtest 

        if(int(priceSTR) > 0):
            prictInt=int(priceSTR)
            qtest= Product.objects.filter(Q(PRDPrice=prictInt))
            if(len(qtest)!= 0):
                query &=qtest
        
        if (len(query) == 0):
            query=Product.objects.all()
        print("****len(query)*****",len(query))
        print("****data(query)*****",query)
        snippets = query
        serializer = productSerializer(snippets, many=True)
        return Response(serializer.data)


# create get all api
@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Product.objects.all()
        paginator = Paginator(snippets, 2) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = productSerializer(page_obj, many=True)
        return Response(serializer.data)

# create get api
@api_view(['GET', 'POST'])
def query_list(request,cat,name):
    snippets = Product.objects.filter(PRDCategory__CATName=cat,PRDName=name)
    serializer = productSerializer(snippets, many=True)
    return Response(serializer.data)

# create get product-details by id
@api_view(['GET'])
def productbyid(request,id):
    snippets = Product.objects.filter(id=id)
    #another query retuen rating from table Rating
    serializer = productSerializer(snippets, many=True)
    return Response(serializer.data)

# create get api categories
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        snippets = Category.objects.all()
        serializer = categorySerializer(snippets, many=True)
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




#get ratingItem for item 
def ratingItem(request,id):
    query = Rating.objects.filter(RATProduct__pk=id)
    sum = 0
    for item in query:
        sum += item.stars
    print(sum)
    return HttpResponse("sum is ="+ str(sum))
    
#get rating from product for item >>
# def 

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


#tiger
@api_view(['GET', 'POST'])
def addp(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    PRDName=body['PRDName']
    PRDCategory = body['PRDCategory']
    PRDDesc = body['PRDDesc']
    PRDImage = body['PRDImage']
    PRDPrice = body['PRDPrice']
    PRDDiscountPrice = body['PRDDiscountPrice']
    PRDCost = body['PRDCost']

    obj=Product()
    obj.PRDName=PRDName
    obj.PRDCategory__CATName = PRDCategory
    obj.PRDDesc = PRDDesc
    obj.PRDImage = PRDImage
    obj.PRDPrice = PRDPrice
    obj.PRDDiscountPrice = PRDDiscountPrice
    obj.PRDCost = PRDCost
    obj.save()
    return HttpResponse("productadd")


#tiger
@api_view(['GET', 'POST'])
def addtocard(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['pid']
    uid=body['uid']
    userobj=User.objects.get(id=uid)
    objproduct=Product.objects.get(id=id)
    objorder=Order()
    objorder.order_user=userobj

    objorder.Orderproduct=objproduct
    objorder.save()
    return HttpResponse("oederdone")



#tiger
@api_view(['GET', 'POST'])
def mycard(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid=body['uid']

    obj=Order.objects.all().filter(order_user=uid)
    print("xxxxxxxxxxxxxxmy cardxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(obj)
    print(obj[0].Orderproduct.id)

    #objorder=obj.Orderproduct__id
    i=0
    data=[]
    while(i<len(obj)):
        objproduct = Product.objects.all().filter(id=obj[i].Orderproduct.id)
    #product=objorder.Orderproduct
        serializer = productSerializer(objproduct, many=True)
        data.append(serializer.data)
        i=i+1

    return Response(data)