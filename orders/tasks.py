from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def OrderCreated(order_id):
    """
    Sending Email of order creating
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order.id)
    message = 'Dear, {}, You have successfully placed an order.\
                   Your order number {}'.format(order.customer_name, order.id)
    mail_send = send_mail(subject, message, 'admin@myshop.ru', [order.customer_email])
    return mail_send