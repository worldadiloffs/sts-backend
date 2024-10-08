

from asyncio.log import logger
from clickApp import ClickUz
from ordersts.models import Order



def create_click_payment(amount:float, order:object ):
    """
    Create click payment
    args: amount, order
    return: url for click `payment
    """
    try:
        order = Order.objects.get(
            total_price=amount,
            order=order
        )
        url = ClickUz.generate_url(order_id=str(order.pk), 
        amount=str(order.total_price))
        return True, url
    except Exception as e:
        logger.error(e)
        return False, e