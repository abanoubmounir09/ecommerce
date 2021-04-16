from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator
from .models import Product,Category,Rating
from .forms import addproductform
#serialize
from .serializers import productSerializer, categorySerializer
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





# rating function 
#@action(detail=True,method=['POST'])
@api_view(['POST'])
def rate_product(request,id=None):
    print('***************',request.data)   
    if 'stars' in request.data:
        product=Product.objects.filter(id=id)
        stars= request.data['stars']
        #user = request.user
        user =User.objects.get(id=1)
        print('user',user)
        try:
            rating = Rating.objects.get(user=user.id ,prodcut=prodcut.id)
            rating.stars = stars
            rating.save()
            serializer=RatingSerializer(rating,many=False)
            response={'message':'Rating Updated','result':serializer.data}
            return Response(response,status=status.HTTP_200_OK)
           

        except:
            rating = Rating.objects.create(user=user,prodcut=prodcut,stars=stars)
            serializer=RatingSerializer(rating,many=False)
            response={'message':'Rating Created','result':serializer.data}
            return Response(response,status=status.HTTP_200_OK)


       
    else:
        response={'message':'You need to provide stars'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
