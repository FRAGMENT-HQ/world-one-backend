
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

# using cash free sdk

x_api_version = "2023-08-01"


class PayoutsView(APIView):
    def post(self, request):
        # Create a client object
        data = request.data
        print(data)
        user = User.objects.filter(email=data['email']).first()
        methord = data["methord"]
        order = Order.objects.filter(id=data['order_id']).first()

        meta = OrderMeta(payment_methods=methord)
        itms =order.order_items.all()
        amount = 0
        for i in itms:
            amount += float(i.inr_amount)



        customerDetails = CustomerDetails(customer_id=f"wf_{user.id}",  customer_phone="9999999999", customer_email=user.email)
        createOrderRequest = CreateOrderRequest(order_amount=int(amount*0.05), order_currency="INR", customer_details=customerDetails,order_meta=meta)
        try:
            api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None).data.__dict__
            

            Payment.objects.create(order=order, cashfree_id=api_response['order_id'], payment_status="pending", payment_request_id=api_response['cf_order_id'], payment_amount=int(amount*0.05))
            return Response({"session": api_response['payment_session_id']})
            
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=400)

        




# Create your views here.
