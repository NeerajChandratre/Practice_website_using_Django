from django.urls import path
from . import views

urlpatterns = [
    path("order/",views.place_order,name="place_order"),
    path("order/<int:order_id>/",views.order_status,name="order_status"),
    path("",views.home,name="home"),
    path("employee/dashboard/",views.employee_dashboard,name="employee_dashboard"),
    path("pizza-chat/", views.pizza_chat, name="pizza_chat"),
    path("check-order/", views.check_order_status, name="check_order_status"),
]
