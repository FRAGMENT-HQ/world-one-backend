
from rest_framework.response import Response
from rest_framework.views import APIView
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from User.models import User
from products.models import Order
from .models import Payment
from rest_framework.permissions import IsAuthenticated
from communication.utils import send_email
import requests
# using cash free sdk

x_api_version = "2023-08-01"
cashfree_url = "https://api.cashfree.com/pg/links"


def genrate_link(order_id, amount, phone_no, email):
    print(amount,order_id)
    amount =1

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-version": "2023-08-01",
        "x-client-id": "649473fea04bd2c52eb3562df5374946",
        "x-client-secret": "cfsk_ma_prod_52f37f75779f043b62de44eb3305b42a_d8cc3965"
        # "x-client-id": "TEST101499510773cdbd8252237d9f0a15994101",
        # "x-client-secret": "cfsk_ma_test_3dc2a88ccedd435bea00346c5fe5b723_a318d218"
    }

    data = {
        "customer_details": {
            "customer_phone": phone_no,
            "customer_email": email
        },
        "link_notify": {
            "send_sms": True,
            "send_email": True
        },
        "link_meta": {
            "upi_intent": False,
            "return_url": f"https://www.worldoneforex.com/payment?check=true"
        },
        "link_id": order_id,
        "link_amount": amount,
        "link_currency": "INR",
        "link_purpose": "pay",
        "link_partial_payments": False,
    }

    response = requests.post(cashfree_url, headers=headers, json=data)
    print(response.json())
    return response.json()

def verify_link(id):
    url = f"{cashfree_url}/{id}"
    headers = {
    "accept": "application/json",
    "x-api-version": "2023-08-01",
    "x-client-id": "649473fea04bd2c52eb3562df5374946",
    "x-client-secret": "cfsk_ma_prod_52f37f75779f043b62de44eb3305b42a_d8cc3965"
    #  "x-client-id": "TEST101499510773cdbd8252237d9f0a15994101",
    #     "x-client-secret": "cfsk_ma_test_3dc2a88ccedd435bea00346c5fe5b723_a318d218"
    }

    print(url)
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()



class PayoutsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data
        user = request.user
        methord = data["methord"]
        partial = bool(data["partial"])

        mul = 1
        if partial:
            mul = 0.05
        order = Order.objects.filter(id=data['order_id']).first()
        if order is None:
            return Response({"error": "Order not found"}, status=404)
        payment_obj = Payment.objects.filter(order=order)
        if (payment_obj.exists()):
            return Response({"link": payment_obj.first().payment_link})

        # meta = OrderMeta(payment_methods=methord)
        itms = order.order_items.all()
        amount = 0
        for i in itms:
            amount += float(i.inr_amount)

        gst = amount * (order.gst_amount-1)

        # customerDetails = CustomerDetails(
        #     customer_id=f"wf_{user.id}",  customer_phone=user.phone_no, customer_email=user.email)
        cba = int(amount*mul + gst)
        order.total_amount = amount + gst
        order.save()

        try:

            """
            sample response

            {
  "cf_link_id": "41342540",
  "customer_details": {
    "customer_name": "",
    "country_code": "+91",
    "customer_phone": "9833290022",
    "customer_email": "pranavleo22@gmail.com"
  },
  "enable_invoice": false,
  "entity": "link",
  "link_amount": 1,
  "link_amount_paid": 0,
  "link_auto_reminders": false,
  "link_created_at": "2024-08-03T02:46:45+05:30",
  "link_currency": "INR",
  "link_expiry_time": "2024-09-02T02:46:45+05:30",
  "link_id": "1234",
  "link_meta": {
    "payment_methods": "cc,dc,upi,nb"
    "upi_intent": "false"
  },
  "link_minimum_partial_amount": null,
  "link_notes": {},
  "link_notify": {
    "send_email": true,
    "send_sms": true
  },
  "link_partial_payments": false,
  "link_purpose": "xxxxxxxxxxxx",
  "link_qrcode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAAFAAQMAAAD3XjfpAAAABlBMVEX///8AAABVwtN+AAAC60lEQVR4nOyaMZLrOAxEW6WAoY6go+hmJn0zHcVHYKhApd7qBr3fnprd6EekEKmkN8GgCKAbNO644447/m6sVEwHNp5YOR3L/sDywpUqsj6dXYIFwDYdCzkf2PT9obcX9BcARgfJ1zaRLEjklcjnubxAcn/MZOkYVIo4Hyt5INKjbzf4L7jsmNvDY+YrT/+Vx07AVjN7PtNrI+t2wb3FefqluMYCW8dd9jwf636luqm4st/81pq7ACM0Z4oaqTpqgUBW/BLjge64+q7iUh71gAsLPZjPLsHM9rrwWHd1EswVbimZdS1jg6vHCxKjpbj16q0e8glkdAoqPak1j8sDp/pPeUmanoODZ+u65UySZBWPua7lcmaXjzE8JIg8kzvfY1jTd3o7nCcrcp8glB4fGvUWVRl0aICFT8v4wUE5F0kyuzgJtRjD0mZz/aPN+gJzE+yuGStSjeGsyfM88WMgDQgivaTNgLD2jM2HtFkm2Se4SnPQ4sOvZO2lOUKtfajSUcEzubiijKhctjEcbrdLEHb00VL4rpkq4xIqpAwO5rlN3qIqU8eVJMvWZsrj2SOo/9+Sa4eKx71FBs7i49PWjwkCEqIS7NFbWvqsQrK6bpdg6HArLSVjiunKcoUKIQcHi6EkaZ7I6S0+kOpGfhdXT6CvjnxODLJ5V81bfBXXmCDQ1jw8ZO09eejzNJ32Kx2C8q6vTZqjqJ1KkU46NB6zsQgcGVz51ma5KVLvy6VI9+l7wz4kWOYjigto+562DqtxUY1uQV+ieDNsaSrLqtTEPB4clKO/UrVyjzGsZuut6dfivCcwYmqrT9sUX7HxbVPGBmMr7C0YYx2G6Vy8NLfJ/XN6ugJ924ywc+v+difZxuWnixsRbD9g2XO7gYwtmK3cdxV2CNY4Pe6fsRAl7V1vMMD40QKlzWrMGeXxYwx3Bbpm4g6eu3eg3vdgiX3P4GB0XNXULD+TqtdhfvCKuEvwjjvuuOP/458AAAD//2VokXg1z9gXAAAAAElFTkSuQmCC",
  "link_status": "ACTIVE",
  "link_url": "https://payments.cashfree.com/links/G74dgl29o42g",
  "order_splits": [],
  "terms_and_conditions": "",
  "thank_you_msg": ""
}

            """
            print(cba)
            api_response = genrate_link(
                f"wf_prod_link_{order.id}", cba, user.phone_no, user.email)

            obj = Payment.objects.create(order=order, cashfree_id=f"wf_prod_link_{order.id}", payment_status="pending",
                                         payment_request_id=api_response['cf_link_id'], payment_amount=cba, payment_link=api_response['link_url'])

            return Response({"link": api_response['link_url']})

        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong"}, status=400)


class confirmation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        order_id = data['order_id']
        order = Order.objects.filter(id=order_id).first()
        payment = Payment.objects.filter(order=order).last()
        try:
            resp = verify_link(payment.cashfree_id)
            if resp["link_amount"] == resp["link_amount_paid"] :
                payment.payment_status = "Sucess"
                payment.save()
                order.amount_paid = resp["link_amount_paid"]

                user = payment.order.user

                send_email("Order Confirmation ",
                           f"Your order with id {payment.order.id} has been confirmed", user.email)
            print(resp)
            return Response({"message": "success"})
        except Exception as e:
            print(e)
            return Response({"message": "failed"})


        

        # order = Order.objects.filter(id=data['order_id']).first()
        # # latest payment object of this order
        # payment = Payment.objects.filter(order=order).last()
        # # payment = Payment.objects.filter(cashfree_id=data['order_id']).first()
        # payment.payment_status = data['status']
        # payment.save()
        # if data['status'] == "SUCCESS":
        #     user =request.user
        #     payment.order.payment_status = "paid"
        #     payment.order.save()
        #     send_email("Order Confirmation", f"Your order with id {payment.order.id} has been confirmed", user.email)
        


class webhook(APIView):
    def post(self, request):
        data = request.data["data"]
        cashfree_id = data["payment"]["cf_payment_id"]
        print(cashfree_id)
        payment = Payment.objects.filter(payment_request_id=cashfree_id)
        if payment.exists():
            payment = payment.first()
            payment.payment_status = "Sucess"
            payment.save()

            user = payment.order.user

            send_email("Order Confirmation",
                       f"Your order with id {payment.order.id} has been confirmed", user.email)
            return Response({"message": "success"})
        else:
            return Response({"message": "failed"})


