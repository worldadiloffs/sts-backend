from asyncio.log import logger
from clickApp.views import ClickUzMerchantAPIView
from clickApp import ClickUz
from ordersts.models import Order


class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        """
        To'langan buyurtmani tekshiring: agar bosgan to'lov haqiqiy bo'lsa
        :param order_id: buyurtma identifikatori
        :param miqdori: summa
        :qaytish: agar buyurtma topilsa va summa yaroqli bo'lsa, ORDER_FOUND qaytaring, aks holda ORDER_NOT_FOUND qaytaring
        :rtype: agar buyurtma topilsa, lekin summa yaroqsiz bo'lsa, INVALID_AMOUNT miqdorini qaytaring
        """
        try:
            print(f'check_order: {order_id}  {amount}')
            order = Order.objects.get(zakas_id=int(order_id))
            if float(order.total_price) == float(amount):
                order.status = 'pending'
                return self.ORDER_FOUND
            else:
                order.status = 'cencel'
                return self.INVALID_AMOUNT
        except Exception as e:
            logger.error(e)
            return self.ORDER_NOT_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
       
        """
        Muvaffaqiyatli to'lov: agar Clint buyurtmani muvaffaqiyatli to'lagan bo'lsa: 
        Bu usulda buyurtma holatini to'langan True ga o'zgartirishimiz mumkin
        :param order_id: buyurtma identifikatori
        :param tranzaksiya: tranzaksiya obyekti
        :qaytish: Yo'q
        """
        try:
            print(f'successfully_payment: {order_id}  {str(transaction)}')
            order = Order.objects.get(zakas_id=int(order_id))
            order.is_finished = True
            order.save()
        except Exception as e:
            logger.error(e)
    
    def cancel_payment(self, order_id: str, transaction: object):
        """
        To'lovni bekor qilish: agar clint to'lovni bekor qilsa
        :param order_id: buyurtma identifikatori
        :param tranzaksiya: tranzaksiya obyekti
        """
        try:
            print(f'cancel_payment: {order_id}  {str(transaction)}')
            order = Order.objects.get(zakas_id=int(order_id))
            order.status = 'cencel'
            order.save()
        except Exception as e:
            logger.error(e)

class TestView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment