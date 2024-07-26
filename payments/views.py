
from rest_framework.response import Response
from rest_framework.views import APIView
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from User.models import User
from products.models import Order
from .models import Payment
import json
from rest_framework.permissions import IsAuthenticated
from communication.utils import send_email

# using cash free sdk

x_api_version = "2023-08-01"


class PayoutsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Create a client object
        data = request.data
        print(data)

        user = request.user
        methord = data["methord"]
        partial = bool(data["partial"])
        mul = 1
        if partial:
            mul = 0.05
        order = Order.objects.filter(id=data['order_id']).first()

        meta = OrderMeta(payment_methods=methord)
        itms = order.order_items.all()
        amount = 0
        for i in itms:
            amount += float(i.inr_amount)

        gst = amount * order.gst_amount
        print(user)

        customerDetails = CustomerDetails(
            customer_id=f"wf_{user.id}",  customer_phone=user.phone_no, customer_email=user.email)
        createOrderRequest = CreateOrderRequest(order_amount=int(
            amount*mul + gst ), order_currency="INR", customer_details=customerDetails, order_meta=meta)
        try:
            api_response = Cashfree().PGCreateOrder(
                x_api_version, createOrderRequest, None, None).data.__dict__
            print(api_response)
            obj=Payment.objects.create(order=order, cashfree_id=api_response['order_id'], payment_status="pending",
                                   payment_request_id=api_response['cf_order_id'], payment_amount=int(amount*0.05))
            print(obj.__dict__)
            return Response({"session": api_response['payment_session_id']})

        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=400)


class confirmation(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        order = Order.objects.filter(id=data['order_id']).first()
        # latest payment object of this order
        payment = Payment.objects.filter(order=order).last()
        # payment = Payment.objects.filter(cashfree_id=data['order_id']).first()
        payment.payment_status = data['status']
        payment.save()
        # if data['status'] == "SUCCESS":
        #     user =request.user
        #     payment.order.payment_status = "paid"
        #     payment.order.save()
        #     send_email("Order Confirmation", f"Your order with id {payment.order.id} has been confirmed", user.email)
        return Response({"message": "success"})

class webhook(APIView):
    def post(self, request):
        data = request.data["data"]
        cashfree_id=data["payment"]["cf_payment_id"]
        print(cashfree_id)
        payment = Payment.objects.filter(payment_request_id=cashfree_id)
        if payment.exists():
            payment = payment.first()
            payment.payment_status = "Sucess"
            payment.save()
        
            user = payment.order.user
        
            send_email("Order Confirmation", f"Your order with id {payment.order.id} has been confirmed", user.email)
            return Response({"message": "success"})
        else:
            return Response({"message": "failed"})

