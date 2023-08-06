
from math import ceil
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import  render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from datetime import datetime
from django.contrib import messages
from .models import Product,Orders,OrderUpdate
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
import razorpay
keyid='rzp_test_FYqvo67zNk6DSr'
keySecret='Pl4QMyOBjXMbg7NkjohzBQf4'


from craft import keys

MERCHANT_KEY=keys.MK


# Create your views here.

def index(request):
    
    return render(request,'index.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)#ye apan ne isiliye likha jisse agar manlo apan ne register ke time pe same username dalke submit kara to unique constraint ka error na ye
        if user.exists():
            messages.info(request,"Username already taken")
            return redirect('register')
             
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        
        user.set_password(password)#this is done so that password is encrypted
        user.save()
        
        messages.info(request,'Account created succesfully')
        
        return redirect('register')
        
    return render(request,'register.html')
    
    

def loginuser(request):
    if request.method=="POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():#ye check karne ke liye ki iss username se user exists karta h ya nhi
            messages.info(request,"Invalid Username ")
            return redirect('loginuser')
        
        user=authenticate(username=username,password=password)#agar username ya password galat hua to ye None return karega
        
        if user is None:
            messages.info(request,"Invalid Password")
            return redirect('loginuser')
        
        else:
            login(request,user)
            return redirect('mainpage')
            
            
        
    return render(request,'index.html')

def logoutuser(request):
    logout(request)
    return redirect('loginuser')

         
     
@login_required(login_url="loginuser")
def mainpage(request):
    return render(request,'mainpage.html')

@login_required(login_url="loginuser")
def dreamcatchers(request):
    products=Product.objects.all()
    
    allProds=[]
    catprods=Product.objects.values('category','id')
    #print(catprods)
    cats={item['category'] for item in catprods}
    #print("categories are ",cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        print(prod)
        n=len(prod)
        nslides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nslides),nslides])
        #print(allProds) 
    params={'allProds':allProds}
    return render(request,'dreamcatchers.html',params)

# @login_required(login_url="loginuser")
# def resinproducts(request):
#     products=Product.objects.all()
#     print(products)
#     return render(request,'resinproducts.html',context={'products':products})

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
# # PAYMENT INTEGRATION

        amount=int(amount)*100
        client = razorpay.Client(auth=(keyid,keySecret))
        callback_url='http://127.0.0.1:8000/handlerequest'

        data = { "amount":amount, "currency": "INR", "receipt": str(Order.order_id),
                "notes":{
                    "name":"craftcatcher",
                    "Payment for":"crafte items"
                }}
        payment = client.order.create(data=data)
        print(payment)
        return render(request,'payment.html',{'payment':payment,'callback_url':callback_url})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    if request.method=="POST":
        payment_id=request.POST.get('razorpay_payment_id')
        order_id=request.POST.get('razorpay_order_id')
        signature=request.POST.get('razorpay_signature')
        print(payment_id,order_id,signature)
    
    return render(request,'dreamcatchers.html')
    
        
    


def gallery(request):
    return render(request,'gallery.html')