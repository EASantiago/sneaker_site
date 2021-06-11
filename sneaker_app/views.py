from typing import Any
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Sum
import bcrypt
import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        logged_user = User.objects.filter(email=email)
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session["user_id"] = logged_user.id
                request.session["user_name"] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/success')
            else:
                messages.error(request,"password and username do not match")
                return redirect('/')
            
        else: 
            messages.error(request,"User does not exist")
            return redirect('/')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, 'success.html', context)

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def edit(request, id):
    errors = User.objects.validate_edit(request.POST)
    if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect(f'/user_profile/{id}')
    else:
        edit_user = User.objects.get(id=id)
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.email = request.POST['email']
        edit_user.phone = request.POST['phone']
        edit_user.save()
        request.session["user_name"] = f"{edit_user.first_name} {edit_user.last_name}"
        return redirect('/success')

def delete(request, id):
    to_delete = User.objects.get(id=id)
    to_delete.delete()
    return redirect('/')

def purchase(request):
    if request.method == 'POST':
        this_product = Product.objects.filter(id=request.POST["id"])
        if not this_product:
            return redirect('/success')
        else:
            quantity = int(request.POST["quantity"])
            total_charge = quantity*(float(this_product[0].price))
            Order.objects.create(quantity_ordered=quantity, total_price=total_charge)
            return redirect('/checkout')
    else:
        return redirect('/success')

def checkout(request):
    last = Order.objects.last()
    price = last.total_price
    full_order = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    full_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    context = {
        'orders':full_order,
        'total':full_price,
        'bill':price,
    }
    return render(request, "checkout.html", context)

# @csrf_exempt
# def create_checkout_session(request, name, price, image):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - capture the payment later
#             # [customer_email] - prefill the email input in the form
#             # For full details see https://stripe.com/docs/api/checkout/sessions/create

#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': '{{product.name}}',
#                         'image': '{{product.image_url}}',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': '{{product.price}}',
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})