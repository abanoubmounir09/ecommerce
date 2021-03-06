from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.paginator import Paginator
from .models import Product,Category,Rating,Order,OwnerProduct,Favorite
from .forms import addproductform
#auth
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
#serialize
from .serializers import productSerializer, categorySerializer, orderSerializer
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
        # paginator = Paginator(snippets, 6) # Show 25 contacts per page.
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        product_list = productSerializer(snippets, many=True)
        context = {'product_list' : product_list.data}
        return Response(context)

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
    print("qqqqqqq",serializer.data)
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
@api_view(['POST'])
def addp(request):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    if  request.data['userid']:
        userId=request.data['userid']
        file=request.data['cover']       
        PRDName=request.data['PRDName']
        PRDCategory = request.data['PRDCategory']
        PRDDesc = request.data['PRDDesc']
        PRDImage = file
        PRDPrice = request.data['PRDPrice']
        PRDDiscountPrice = request.data['PRDDiscountPrice']
        PRDCost = request.data['PRDCost']
        PRDQuantity= request.data['PRDQuantity']
        newcat=request.data['newcat']

        print("*******reuest data**********",request.data)

        if PRDCategory != 'null' :
            realcategory = Category.objects.get(CATName=PRDCategory)

        obj=Product()

        if newcat:
            catob = Category.objects.filter(CATName=newcat)
            if (len(catob)<=0):
                objcat=Category()
                objcat.CATName=newcat
                objcat.save()
                catob = Category.objects.get(CATName=newcat)
                obj.PRDCategory = catob
                
            obj.PRDCategory = catob
        else:
            obj.PRDCategory = realcategory

        obj.PRDName=PRDName
        obj.PRDDesc = PRDDesc
        obj.PRDImage = PRDImage
        obj.PRDPrice = PRDPrice
        obj.PRDDiscountPrice = PRDDiscountPrice
        obj.PRDCost = PRDCost
        obj.PRDQuantity=PRDQuantity
        obj.save()
        #object from owner product
        user1=User.objects.get(pk=userId)
        ownerObject=OwnerProduct.objects.create(OwnerQuantity=PRDQuantity,OwnerUser=user1,Ownerproduct=obj)
        response={'message':'product added'}
        return Response(response,status=status.HTTP_200_OK)
    else:
        response={'message':'error in added product'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)




#edit item
@api_view(['POST'])
def editItem(request):
    print("*********data********",request.data)
    file=request.data['cover']    
    PRDName=request.data['PRDName']
    PRDCategory = request.data['PRDCategory']
    PRDDesc = request.data['PRDDesc']
    PRDImage = file

    PRDPrice = request.data['PRDPrice']
    PRDDiscountPrice = request.data['PRDDiscountPrice']
    PRDCost = request.data['PRDCost']
    PRDQuantity= request.data['PRDQuantity']
    # newcat=request.data['newcat']

    catob = Category.objects.get(CATName=PRDCategory)


    item = Product.objects.get(id=request.data['PRDId'])
    item.PRDName=PRDName
    item.PRDCategory = catob
    item.PRDDesc = PRDDesc
    item.PRDImage = PRDImage
    item.PRDPrice = PRDPrice
    item.PRDDiscountPrice = PRDDiscountPrice
    item.PRDCost = PRDCost
    item.PRDQuantity=PRDQuantity
    item.save()
    
    response={'message':'product added'}
    return Response(response,status=status.HTTP_200_OK)

#add to card-----------------------------
@api_view(['GET', 'POST'])
def addtocard(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print("bodyyyy",body)
    id = body['pid']
    uid=body['uid']
    q=body['quantity']
    obj=Order.objects.filter( Orderproduct__id=id,order_user=uid)
    if not obj:
        userobj=User.objects.get(id=uid)
        objproduct=Product.objects.get(id=id)
        objorder=Order()
        objorder.order_user=userobj
        objorder.order_quantity=q
        objorder.Orderproduct=objproduct
        objorder.save()
    return HttpResponse("oederdone")


#add to favoriteItem-----------------------------
@api_view(['GET', 'POST'])
def favoriteItem(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print("bodyyyy",body)
    id = body['pid']
    uid=body['uid']
    obj=Favorite.objects.filter( FAVproduct__id=id,Favorite_user=uid)
    if not obj:
        userobj=User.objects.get(id=uid)
        objproduct=Product.objects.get(id=id)
        FAV_item=Favorite()
        FAV_item.FAVproduct=objproduct
        FAV_item.Favorite_user=userobj
        FAV_item.save()
    return HttpResponse("oederdone")


#tiger
@api_view(['GET', 'POST'])
def delonefromcard(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['pid']
    uid=body['uid']
    q=body['quantity'] 
    obj=Order.objects.get( Orderproduct__id=id,order_user=uid)
    obj.order_quantity=q
    obj.save()
    return HttpResponse("done")
    
#tiger
@api_view(['GET', 'POST'])
def mycard(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid=body['uid']
    obj=Order.objects.all().filter(order_user=uid)
    

    #objorder=obj.Orderproduct__id
    print(obj)
    print(obj[0].Orderproduct.id)
    i=0
    data=[]
    quan=[]
    while(i<len(obj)):
        objproduct = Product.objects.all().filter(id=obj[i].Orderproduct.id)
        serializer = productSerializer(objproduct, many=True)
        data.append(serializer.data)
        quan.append(obj[i].order_quantity)
        i=i+1
        
    dic={}
    dic['d']=data
    dic['q']=quan
    return Response(dic)


#tiger
@api_view(['POST'])
def del_after_buy(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid=body['uid']
    i=0
    obj=Order.objects.all().filter(order_user=uid)
    print("order obj",obj)
    while(i<len(obj)):
        q=obj[i].order_quantity
        d=obj[i].Orderproduct.id
        objproduct=Product.objects.get(id=d)
        objproduct.PRDQuantity=objproduct.PRDQuantity-q

        objowner=OwnerProduct.objects.get(Ownerproduct=d)
        objowner.OwnerQuantity=objowner.OwnerQuantity-q
        
        i=i+1
        objproduct.save()
        objowner.save()
    obj.delete()    
    return HttpResponse("done")    
        

#tiger
@api_view(['GET', 'POST'])
def delitemfromcard(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid = body['uid']
    pid=body['pid']
    obj=Order.objects.all().filter(Orderproduct=pid,order_user=uid)
    obj.delete()
    return HttpResponse("item deleted")

#show business account products
@api_view(['POST'])
def owenerProduct(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # print("====user=======",request.data['uid'])
    if request.data['is_staff']:
        ownerobj=OwnerProduct.objects.filter(OwnerUser=request.data['uid'])
        if(len(ownerobj)>0):
            op=ownerobj[0].Ownerproduct.pk
            productarr=[]
            i=0
            while (i<len(ownerobj)):
                filteredproduct=Product.objects.get(pk=ownerobj[i].Ownerproduct.pk)
                productarr.append(filteredproduct)
                i+=1
            serializer =productSerializer(productarr, many=True)
            return Response(serializer.data)
    else:
        response={'message':'user no product'}
        return Response(response,status=status.HTTP_200_OK)
    
#getFavoriteItems
@api_view(['POST'])
def getFavoriteItems(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    if request.data['uid']:
        favorite_items=Favorite.objects.filter(Favorite_user=request.data['uid'])
        if(len(favorite_items)>0):
            op=favorite_items[0].Favorite_user.pk
            productarr=[]
            i=0
            while (i<len(favorite_items)):
                filteredproduct=Product.objects.get(pk=favorite_items[i].FAVproduct.pk)
                productarr.append(filteredproduct)
                i+=1
            serializer =productSerializer(productarr, many=True)
            print("------serializer.data-------",serializer.data)
            return Response(serializer.data)
    else:
        response={'message':'user no product'}
        return Response(response,status=status.HTTP_200_OK)


#deletFavoriteItem
@api_view(['GET', 'POST'])
def deletFavoriteItem(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    uid = body['uid']
    itemId=body['itemId']
    obj=Favorite.objects.all().filter(FAVproduct=itemId,Favorite_user=uid)
    obj.delete()
    return HttpResponse("item deleted")

   

      # prd = Product.objects.create(PRDName="h1",PRDCategory__CATName = 'apple',
        # PRDDesc="ttt",PRDImage=file,PRDPrice="25",PRDDiscountPrice="2",PRDCost="5",PRDQuantity="3")
# def addproduct(request):
#     if request.method == 'POST':
#         obproduct=Product()
#         form = addproductform(request.POST,request.FILES)
#         if form.is_valid():
#             newproduct = form.save(commit=False)
#             newproduct.save()
#         return  HttpResponse('item added')

#     else:
#          form = addproductform()
#          return render(request,'new_product.html',{'form':form})

    # PRDName=body['PRDName']
    # PRDCategory = body['PRDCategory']
    # PRDDesc = body['PRDDesc']
    # PRDImage = body['PRDImage']
    # PRDPrice = request.data['PRDPrice']
    # PRDDiscountPrice = request.data['PRDDiscountPrice']
    # PRDCost = request.data['PRDCost']
    # PRDQuantity= request.data['PRDQuantity']

#get rating from product for item >>
# def 


# #add product in tow tables owner and product
# @api_view(['POST'])
# def addp(request):
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
    
#     userId=request.data['userid']
#     file=request.data['cover']       
#     PRDName=request.data['PRDName']
#     PRDCategory = request.data['PRDCategory']
#     PRDDesc = request.data['PRDDesc']
#     PRDImage = file
#     PRDPrice = request.data['PRDPrice']
#     PRDDiscountPrice = request.data['PRDDiscountPrice']
#     PRDCost = request.data['PRDCost']
#     PRDQuantity= request.data['PRDQuantity']
#     newcat=request.data['newcat']

#     print("*******reuest data**********",request.data)
#     obj=Product()

#     if PRDCategory != 'null' :
#         print("***PRDCategory/////////",PRDCategory)
#         realcategory = Category.objects.get(CATName=PRDCategory)
#         obj.PRDCategory = realcategory

#     elif  newcat != 'undefined' :
#         try:
#             print("***from try if catob/////////",catob)
#             catob = Category.objects.get(CATName=newcat)
#             obj.PRDCategory = catob
#         except:
#             objcat=Category()
#             objcat.CATName=newcat
#             objcat.save()
#             # catob = Category.objects.get(CATName=newcat)
#             # print("***from if catob/////////",catob)
#             obj.PRDCategory__CATName = newcat    

#     obj.PRDName=PRDName
#     obj.PRDDesc = PRDDesc
#     obj.PRDImage = PRDImage
#     obj.PRDPrice = PRDPrice
#     obj.PRDDiscountPrice = PRDDiscountPrice
#     obj.PRDCost = PRDCost
#     obj.PRDQuantity=PRDQuantity
#     obj.save()
#     #object from owner product
#     user1=User.objects.get(pk=userId)
#     ownerObject=OwnerProduct.objects.create(OwnerQuantity=PRDQuantity,OwnerUser=user1,Ownerproduct=obj)
#     esponse={'message':'product added'}
#     # return Response(response,status=status.HTTP_200_OK)
#     # else:
#     response={'message':'error in added product'}
#     return Response(response,status=status.HTTP_400_BAD_REQUEST)


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


