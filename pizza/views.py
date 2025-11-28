from django.shortcuts import render, redirect
from .forms import PizzaOrderForm
from .models import PizzaOrder
from .agents import ai_choose_ingredents_step
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def pizza_chat(request):
    if request.method == "POST":
        user_msg = request.POST.get("message","")
        customer_name = request.POST.get("customer_name", "Guest")
        ai_response = ai_choose_ingredents_step(user_msg)
        if ai_response["status"] == "ok":
            form_data = {
                "customer_name": customer_name,
                "user_descriptn":user_msg
            }
            form = PizzaOrderForm(form_data)
            if form.is_valid():
                print("inside form.is_valid()")
                order = form.save()

                res = ai_response
                ingrednts = res["ingredients"]
                order.ingrednts = ", ".join(ingrednts)
                order.chef_assigned = True
                order.status = "making"
                order.save()

                return JsonResponse({
                    "ai_message": "Your order is confirmed!",
                    "order_id": order.id
                })
        elif ai_response["status"] == "clarification":
            return JsonResponse({
                "ai_message":ai_response.get("message",str(ai_response))
            })

    return render(request, "pizza/pizza_chat.html")

def place_order(request):
    if request.method == "POST":
        print("inside POST")
        form = PizzaOrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            res = ai_choose_ingredents_step(order.user_descriptn)
            ingrednts = res["ingredients"]
            order.ingrednts = ", ".join(ingrednts)
            order.chef_assigned = True
            order.status = "making"
            order.save()

            return redirect("order_status",order_id = order.id)
    else:
        print("outside POST")
        form = PizzaOrderForm()
    
    return render(request,"pizza/order_form.html",{"form":form})

def check_order_status(request):
    status  = None
    error = None

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        if order_id:
            try:
                order= PizzaOrder.objects.get(id=int(order_id))
                status = order.get_status_display()
            except:
                error = "We can't find the order number"
        else:
            error = "Please enter an order number"
    
    return render(request,"pizza/check_order.html",{"status": status, "error": error})


def order_status(request,order_id):
    order = PizzaOrder.objects.get(id=order_id)
    return render(request,"pizza/order_status.html",{"order":order})

def home(request):
    return render(request,"pizza/home.html")

def employee_dashboard(request):
    context = {
        "stock": {
            "Mozzarella_cheese": 450, # cheese starts here
            "Asiago_cheese": 3000,
            "Blue_cheese": 5000,
            "Cheddar_cheese": 6000,
            "Colby_Jack_cheese":5000,
            "Cottage_cheese":2000,
            "Paneer_cheese":3000, #cheese ends here
            "bell_pepper": 120, # vegetables start here
            "capsicum": 150,
            "potato": 200,
            "onion":100,
            "ginger": 20,
            "garlic": 50,
            "corn":100,
            "tomato":300,
            "White_button_mushroom":100,
            "baby_corn":100,
            "green_chilli":100,   # vegetables end here
            "cinnamon":60,     # spices start here,
            "italian_seasoning":30,
            "basil":50,
            "oregano":60,
            "parsley":70,
            "rosemary":80,
            "black_pepper":90,
            "cumin":30,
            "paprika":80  # spices end here
        },
        # "today_sales":80,
        # "profit":4300,
    }
    return render(request,"pizza/employee_dashboard.html",context)


# Create your views here.
