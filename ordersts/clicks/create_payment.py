
from asyncio.log import logger

from clickApp import ClickUz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ordersts.models import Order


class ClickTransactionPayment(APIView):
    """
    Create click payment POST
    args: amount, order
    return: url for click `payment
    """

    def post(self, request):
        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(
                # amount=request.data.get('amount'),
                id = order_id

            )
            # orders=  OrderPayment.objects.get(id=order_id)
            url = ClickUz.generate_url(order_id=str(order.pk), 
            amount=str(order.total_price), return_url="https://sts-hikvision.vercel.app/uz/profile/orders")
            print(url)
            data = {"success": True,'url': url}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"success": False,'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

create_click_payment = ClickTransactionPayment.as_view()


