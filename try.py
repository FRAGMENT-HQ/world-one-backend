from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta




Cashfree.XClientId = "TEST101499510773cdbd8252237d9f0a15994101"
Cashfree.XClientSecret = "cfsk_ma_test_3dc2a88ccedd435bea00346c5fe5b723_a318d218"
Cashfree.XEnvironment = Cashfree.XSandbox
x_api_version = "2023-08-01"

def create_order():
        customerDetails = CustomerDetails(customer_id="123", customer_phone="9999999999")
        orderMeta = OrderMeta(payment_methods="upi")
        createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails,order_meta=orderMeta)

        try:
            api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
            print(api_response.data)

        except Exception as e:
            print(e)
create_order()



xxx="""

version: "3"
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: worldone
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: PaSSword
    volumes:
      - ./db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
  backend:
    build:
      context: ./world-one-backend
      dockerfile: Dockerfile
    working_dir: /usr/wobu

    env_file:
      - ./world-one-backend/.env
    volumes:
        - ./world-one-backend:/usr/wobu
    expose:
      - 9069
    ports:
      - "9069:9069"
    environment:
      DATABASE_URL: postgres://admin:PaSSword@db:5432/worldone
      REDIS_HOST : redis
    depends_on:
      - db
  
  frontend:
      build:
        context: ./world-one-frontend
        dockerfile: Dockerfile
      working_dir: /usr/world-one-frontend

      expose:
        - 4569
      ports:
        - "4569:4569"

volumes:
  # static-ui-content:
  static-ui-content:


"""

"""

upstream wba {
    server localhost:9069;
}

server {

        index index.html index.htm index.nginx-debian.html;
        server_name backend.worldoneforex.com ;

        location ~ / {
                proxy_set_header X-Forwarded-For $remote_addr;
                proxy_set_header Host $http_host;
                proxy_pass         http://wba ;
        }

}






            sudo certbot --nginx -d worldoneforex.com -d www.worldoneforex.com                                                                                                                                                                   

"""