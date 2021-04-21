from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator
from .models import Product,Category,Rating,Order,OwnerProduct
from .forms import addproductform
#auth
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
#serialize
from .serializers import productSerializer, categorySerializer,ownerProductSerializer,RatingSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
        query=Product.objects.all()
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
      
        snippets = query
        serializer = productSerializer(snippets, many=True)
        return Response(serializer.data)


# create get all api
@api_view(['GET', 'POST'])
def snippet_list(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    print("*************requested user is ",request.user)
    if request.method == 'GET':
        snippets = Product.objects.all()
        paginator = Paginator(snippets, 6) # Show 25 contacts per page.
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    print("*************in detais requested user is/////////////// ",request.user)
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


# rating function 

@api_view(['POST'])
def rate_product(request,id=None):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    usernameget=request.data['uname']
    user =User.objects.get(username=usernameget)
    
    if 'stars' in request.data:
        product=Product.objects.get(id=request.data['prdId'])
        stars= request.data['stars']
        user =User.objects.get(username=usernameget)
        try:
            rating = Rating.objects.get(RATUser=user.id ,RATProduct=product.id)
            rating.stars = stars
            rating.save()
            serializer=RatingSerializer(rating,many=False)
            response={'message':'Rating Updated','result':serializer.data}
            return Response(response,status=status.HTTP_200_OK)
        except:
            rating = Rating.objects.create(RATUser=user,RATProduct=product,stars=stars)
            serializer=RatingSerializer(rating,many=False)
            response={'message':'Rating Created','result':serializer.data}
            return Response(response,status=status.HTTP_200_OK)
    else:
        response={'message':'You need to provide stars'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

#add product in tow tables owner and product
@api_view(['GET', 'POST'])
def addp(request,*args,**kwargs):
    print('-------------------',request.data)
    print('-------********------------',request.data['cover'])
    print('-------****PRDName****------------',request.data['PRDName'])

    file=request.data['cover']
    PRDName=request.data['PRDName']
    PRDCategory = request.data['PRDCategory']
    PRDDesc = request.data['PRDDesc']
    PRDImage = file
    PRDPrice = "50"
    PRDDiscountPrice = "3"
    PRDCost = "2"
    PRDQuantity= "3"

    catob = Category.objects.get(CATName=PRDCategory)

    # PRDName=body['PRDName']
    # PRDCategory = body['PRDCategory']
    # PRDDesc = body['PRDDesc']
    # PRDImage = body['PRDImage']
    # PRDPrice = body['PRDPrice']
    # PRDDiscountPrice = body['PRDDiscountPrice']
    # PRDCost = body['PRDCost']
    # PRDQuantity= body['PRDQuantity']
    

    obj=Product()
    obj.PRDName=PRDName
    obj.PRDCategory = catob
    obj.PRDDesc = PRDDesc
    obj.PRDImage = PRDImage
    obj.PRDPrice = PRDPrice
    obj.PRDDiscountPrice = PRDDiscountPrice
    obj.PRDCost = PRDCost
    obj.PRDQuantity=PRDQuantity
    obj.save()
    #object from owner product
    # user1=User.objects.get(pk=2)
    # ownerObject=OwnerProduct.objects.create(OwnerQuantity=PRDQuantity,OwnerUser=user1,OwnerProduct=obj)
    return HttpResponse("productadd")



#add to card-----------------------------
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

#show business account products
@api_view(['POST'])
def owenerProduct(request):
    ownerobj=OwnerProduct.objects.filter(OwnerUser=2)
    op=ownerobj[0].Ownerproduct.pk
    productarr=[]
    i=0
    while (i<len(ownerobj)):
        filteredproduct=Product.objects.get(pk=op)
        productarr.append(filteredproduct)
        i+=1
    serializer =productSerializer(productarr, many=True)
    print('*********************',serializer.data)
    return Response(serializer.data)
    
   



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

# def showproduct(request):
#     obj=Product.objects.all()
#     return render(request,'home.html',{'data':obj})

"""
    category_list= Category.objects.filter(product__PRDName='note 11')
    print('**************',category_list)
    print(list_samsung)
    return HttpResponse(list_samsung.first())
"""

